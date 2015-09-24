from django.contrib.auth import authenticate
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q
from django.template.defaultfilters import slugify


from submission import forms
from core import models as core_models
from core import log
from core import logic as core_logic
from submission import logic
from submission import models as submission_models
from manager import forms as manager_forms


import mimetypes as mime
from uuid import uuid4
import os
from pprint import pprint
import json

@login_required
def start_submission(request, book_id=None):

	ci_required = core_models.Setting.objects.get(group__name='general', name='ci_required')
	checklist_items = submission_models.SubmissionChecklistItem.objects.all()

	if book_id:
		book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
		book_form = forms.SubmitBookStageOne(instance=book, ci_required=ci_required.value)
		checklist_form = forms.SubmissionChecklist(checklist_items=checklist_items, book=book)
	else:
		book = None
		book_form = forms.SubmitBookStageOne()
		checklist_form = forms.SubmissionChecklist(checklist_items=checklist_items)

	if request.method == 'POST':
		if book:
			book_form = forms.SubmitBookStageOne(request.POST, instance=book, ci_required=ci_required.value)
		else:
			book_form = forms.SubmitBookStageOne(request.POST, ci_required=ci_required.value)

		checklist_form = forms.SubmissionChecklist(request.POST, checklist_items=checklist_items)

		if book_form.is_valid() and checklist_form.is_valid():
			book = book_form.save(commit=False)
			book.owner = request.user
			if not book.submission_stage > 2:
				book.submission_stage = 2
				book.save()
				log.add_log_entry(book, request.user, 'submission', 'Submission Started', 'Submission Started')
			book.save()

			if not book_id and book:
				if book.book_type == 'monograph':
					logic.copy_author_to_submission(request.user, book)
				elif book.book_type == 'edited_volume':
					logic.copy_editor_to_submission(request.user, book)
			return redirect(reverse('submission_two', kwargs={'book_id': book.id}))

	template = "submission/start_submission.html"
	context = {
		'book_form': book_form,
		'checklist_form': checklist_form,
		'book': book,
		'active': 1,
	}

	return render(request, template, context)

@login_required
def submission_two(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	book_form = forms.SubmitBookStageTwo(instance=book)

	logic.check_stage(book.submission_stage, 2)

	if request.method == 'POST':
		book_form = forms.SubmitBookStageTwo(request.POST, instance=book)
		if book_form.is_valid():
			book = book_form.save(commit=False)
			if not book.submission_stage > 3:
				book.submission_stage = 3
			book.save()
			return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = "submission/submission_two.html"
	context = {
		'book': book,
		'book_form': book_form,
		'active': 2,
	}

	return render(request, template, context)

@login_required
def submission_three(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)
	manuscript_files = core_models.File.objects.filter(book=book, kind='manuscript')
	additional_files = core_models.File.objects.filter(book=book, kind='additional')

	logic.check_stage(book.submission_stage, 3)

	if request.method == 'POST':
		if 'manuscript_upload' in request.POST:
			for file in request.FILES.getlist('manuscript_file'):
				handle_file(file, book, 'manuscript', request.user)
			return redirect(reverse('submission_additional_files', kwargs={'book_id': book.id, 'file_type': 'manuscript_files'}))

		if 'additional_upload' in request.POST:
			for file in request.FILES.getlist('additional_file'):
				handle_file(file, book, 'additional', request.user)
			return redirect(reverse('submission_additional_files', kwargs={'book_id': book.id, 'file_type': 'additional_files'}))

		if 'next_stage' in request.POST:
			if manuscript_files.count() >= 1:
				if not book.submission_stage > 4:
					book.submission_stage = 4
				book.save()
				return redirect(reverse('submission_four', kwargs={'book_id': book.id}))
			else:
				messages.add_message(request, messages.ERROR, 'You must upload a Manuscript File.')

		# Catch, after any post we always redirect to avoid someone resubmitting the same file twice.
		return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = 'submission/submission_three.html'
	context = {
		'book': book,
		'active': 3,
		'manuscript_files': manuscript_files,
		'additional_files': additional_files,
	}

	return render(request, template, context)

@login_required
def submission_additional_files(request, book_id, file_type):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if file_type == 'additional_files':
		files = core_models.File.objects.filter(book=book, kind='additional')
	elif file_type == 'manuscript_files':
		files = core_models.File.objects.filter(book=book, kind='manuscript')

	if request.POST:
		for _file in files:
			_file.label = request.POST.get('label_%s' % _file.id)
			_file.save()
		return redirect(reverse('submission_three', kwargs={'book_id': book.id}))

	template = 'submission/submission_additional_files.html'
	context = {
		'book': book,
		'files': files,
	}

	return render(request, template, context)

@login_required
def submission_four(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	logic.check_stage(book.submission_stage, 4)

	if request.method == 'POST' and 'next_stage' in request.POST:
		if book.author.count() >= 1 or book.editor.count() >= 1:
			if not book.submission_stage > 5:
				book.submission_stage = 5
				book.save()
			return redirect(reverse('submission_five', kwargs={'book_id': book.id}))
		else:
			messages.add_message(request, messages.ERROR, 'You must add at least one author or editor.')

	template = 'submission/submission_four.html'
	context = {
		'book': book,
		'active': 4,
	}

	return render(request, template, context)

@login_required
def submission_five(request, book_id):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	logic.check_stage(book.submission_stage, 5)

	if request.method == 'POST' and 'complete' in request.POST:
		book.submission_date = timezone.now()
		book.slug = slugify(book.title)
		stage = core_models.Stage(current_stage='submission', submission=book.submission_date)
		stage.save()
		book.stage = stage
		book.save()
		log.add_log_entry(book, request.user, 'submission', 'Submission of %s completed' % book.title, 'Submission Completed')
		return redirect(reverse('user_home'))

	template = 'submission/submission_five.html'
	context = {
		'book': book,
		'active': 5,
		'manuscript_files': core_models.File.objects.filter(book=book, kind='manuscript'),
		'additional_files': core_models.File.objects.filter(book=book, kind='additional'),
	}

	return render(request, template, context)

@login_required
def author(request, book_id, author_id=None):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if author_id:
		if book.author.filter(pk=author_id).exists():
			author = get_object_or_404(core_models.Author, pk=author_id)
			author_form = forms.AuthorForm(instance=author)
		else:
			return HttpResponseForbidden()
	else:
		author = None
		author_form = forms.AuthorForm()

	if request.method == 'POST':
		if author:
			author_form = forms.AuthorForm(request.POST, instance=author)
		else:
			author_form = forms.AuthorForm(request.POST)
		if author_form.is_valid():
			author = author_form.save(commit=False)
			if not author.sequence:
				author.sequence = 1
			author.save()
			if not author_id:
				book.author.add(author)

			return redirect(reverse('submission_four', kwargs={'book_id': book.id}))

	template = "submission/author.html"
	context = {
		'author_form': author_form,
		'book': book,
	}

	return render(request, template, context)

@login_required
def editor(request, book_id, editor_id=None):
	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if editor_id:
		if book.editor.filter(pk=editor_id).exists():
			editor = get_object_or_404(core_models.Editor, pk=editor_id)
			editor_form = forms.EditorForm(instance=editor)
		else:
			return HttpResponseForbidden()
	else:
		editor = None
		editor_form = forms.EditorForm()

	if request.method == 'POST':
		if editor:
			editor_form = forms.EditorForm(request.POST, instance=editor)
		else:
			editor_form = forms.EditorForm(request.POST)
		if editor_form.is_valid():
			editor = editor_form.save(commit=False)
			if not editor.sequence:
				editor.sequence = 1
			editor.save()
			if not editor_id:
				book.editor.add(editor)

			return redirect(reverse('submission_four', kwargs={'book_id': book.id}))

	template = "submission/editor.html"
	context = {
		'author_form': editor_form,
		'book': book,
	}

	return render(request, template, context)

@login_required
def start_proposal(request):

	proposal_form_id = core_models.Setting.objects.get(name='proposal_form').value
	proposal_form = manager_forms.GeneratedForm(form=core_models.ProposalForm.objects.get(pk=proposal_form_id))
	default_fields = manager_forms.DefaultForm()

	if request.method == 'POST':
		proposal_form = manager_forms.GeneratedForm(request.POST,form=core_models.ProposalForm.objects.get(pk=proposal_form_id))
		default_fields = manager_forms.DefaultForm(request.POST)
		if proposal_form.is_valid() and default_fields.is_valid():
			save_dict = {}
			file_fields = core_models.ProposalFormElement.objects.filter(proposalform=core_models.ProposalForm.objects.get(pk=proposal_form_id), field_type='upload')
			data_fields = core_models.ProposalFormElement.objects.filter(~Q(field_type='upload'), proposalform=core_models.ProposalForm.objects.get(pk=proposal_form_id))

			for field in file_fields:
				if field.name in request.FILES:
					# TODO change value from string to list [value, value_type]
					save_dict[field.name] = [handle_proposal_file(request.FILES[field.name], submission, review_assignment, 'reviewer')]

			for field in data_fields:
				if field.name in request.POST:
					# TODO change value from string to list [value, value_type]
					save_dict[field.name] = [request.POST.get(field.name), 'text']

			defaults = {field.name: field.value() for field in default_fields}
			json_data = json.dumps(save_dict)
			proposal = submission_models.Proposal(form=core_models.ProposalForm.objects.get(pk=proposal_form_id), data=json_data, owner=request.user, **defaults)
			proposal.save()
			messages.add_message(request, messages.SUCCESS, 'Proposal %s submitted' % proposal.id)
			return redirect(reverse('user_home'))


	template = "submission/start_proposal.html"
	context = {
		'proposal_form': proposal_form,
		'default_fields': default_fields
	}

	return render(request, template, context)

@login_required
def proposal_revisions(request, proposal_id):

	proposal = get_object_or_404(submission_models.Proposal, pk=proposal_id, owner=request.user, status='revisions_required')
	proposal_form = forms.SubmitProposal(instance=proposal)

	if request.POST:
		proposal_form = forms.SubmitProposal(request.POST, request.FILES, instance=proposal)
		if proposal_form.is_valid():
			proposal = proposal_form.save(commit=False)
			proposal.status = 'revisions_submitted'
			proposal.save()
			messages.add_message(request, messages.SUCCESS, 'Revisions for Proposal %s submitted' % proposal.id)
			return redirect(reverse('user_home'))

	template = "submission/start_proposal.html"
	context = {
		'proposal_form': proposal_form,
	}

	return render(request, template, context)


## File helpers
def handle_file(file, book, kind, user):

	original_filename = str(file._get_name())
	filename = str(uuid4()) + '.' + str(os.path.splitext(original_filename)[1])
	folder_structure = os.path.join(settings.BASE_DIR, 'files', 'books', str(book.id))

	if not os.path.exists(folder_structure):
		os.makedirs(folder_structure)

	path = os.path.join(folder_structure, str(filename))
	fd = open(path, 'wb')
	for chunk in file.chunks():
		fd.write(chunk)
	fd.close()

	file_mime = mime.guess_type(filename)

	try:
		file_mime = file_mime[0]
	except IndexError:
		file_mime = 'unknown'

	if not file_mime:
		file_mime = 'unknown'

	new_file = core_models.File(
		mime_type=file_mime,
		original_filename=original_filename,
		uuid_filename=filename,
		stage_uploaded=1,
		kind=kind,
		owner=user,
	)
	new_file.save()
	book.files.add(new_file)
	book.save()


	return path

# AJAX handler
@csrf_exempt
@login_required
def file_order(request, book_id, type_to_handle):

	book = get_object_or_404(core_models.Book, pk=book_id, owner=request.user)

	if type_to_handle == 'manuscript':
		id_to_get = 'man'
		files = core_models.File.objects.filter(book=book, kind='manuscript')
	elif type_to_handle == 'additional':
		id_to_get = 'add'
		files = core_models.File.objects.filter(book=book, kind='additional')
	elif type_to_handle == 'author':
		id_to_get = 'auth'
		files = core_models.Author.objects.filter(book=book)
	elif type_to_handle == 'editor':
		id_to_get = 'edit'
		files = core_models.Editor.objects.filter(book=book)

	if request.POST:
		ids = request.POST.getlist('%s[]' % id_to_get)
		ids = [int(_id) for _id in ids]
		for file in files:
			# Get the index:
			file.sequence = ids.index(file.id)
			file.save()

	return HttpResponse('Thanks')
