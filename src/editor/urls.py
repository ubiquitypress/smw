from django.conf.urls import url

from .views import (
    add_chapter,
    add_chapter_format,
    add_edit_chapter_author,
    add_format,
    add_physical,
    add_review_files,
    assign_copyeditor,
    assign_indexer,
    assign_typesetter,
    catalog,
    catalog_marc21,
    contract_manager,
    decline_submission,
    delete_contributor,
    delete_format_or_chapter,
    delete_review_files,
    editor_add_editors,
    editor_add_note,
    editor_add_reviewers,
    editor_change_owner,
    editor_change_revision_due_date,
    editor_dashboard,
    editor_decision,
    editor_editing,
    editor_notes,
    editor_production,
    editor_publish,
    editor_review,
    editor_review_assignment,
    editor_review_round,
    editor_review_round_cancel,
    editor_review_round_remove,
    editor_review_round_reopen,
    editor_review_round_withdraw,
    editor_status,
    editor_submission,
    editor_tasks,
    editor_update_note,
    editor_view_editorial_review,
    editor_view_revisions,
    files_for_production,
    hide_review,
    identifiers,
    new_submissions,
    published_books,
    remove_assignment_editor,
    request_revisions,
    retailers,
    update_chapter,
    update_contributor,
    update_format_or_chapter,
    update_review_due_date,
    view_chapter,
    view_chapter_format,
    view_copyedit,
    view_index,
    view_new_submission,
    view_typesetter,
    view_typesetter_alter_author_due,
    view_typesetter_alter_due_date,
)

urlpatterns = [
    url(  # Review.
        r'dashboard/$',
        editor_dashboard,
        name='editor_dashboard'
    ),
    url(
        r'dashboard/published/$',
        published_books,
        name='editor_published_books'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/$',
        editor_submission,
        name='editor_submission'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/add/editors/$',
        editor_add_editors,
        name='editor_add_editors'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/change/owner/$',
        editor_change_owner,
        name='editor_change_owner'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/tasks/$',
        editor_tasks,
        name='editor_tasks'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/status/$',
        editor_status,
        name='editor_status'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/decision/(?P<decision>[-\w]+)/$',
        editor_decision,
        name='editor_decision'
    ),

    url(
        r'^submission/(?P<submission_id>\d+)/notes/$',
        editor_notes,
        name='editor_notes'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/notes/(?P<note_id>\d+)/$',
        editor_notes,
        name='editor_notes_view'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/notes/update/(?P<note_id>\d+)/$',
        editor_update_note,
        name='editor_notes_update'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/notes/add$',
        editor_add_note,
        name='editor_notes_add'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/$',
        editor_review,
        name='editor_review'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_number>\d+)/$',
        editor_review_round,
        name='editor_review_round'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_number>\d+)/cancel/$',
        editor_review_round_cancel,
        name='editor_review_round_cancel'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_number>\d+)/delete/(?P<review_id>\d+)/$',
        editor_review_round_remove,
        name='editor_review_round_remove'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_number>\d+)/reopen/(?P<review_id>\d+)/$',
        editor_review_round_reopen,
        name='editor_review_round_reopen'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_number>\d+)/withdraw/(?P<review_id>\d+)/$',
        editor_review_round_withdraw,
        name='editor_review_round_withdraw'
    ),
    url(  # Editorial.
        r'submission/(?P<submission_id>\d+)/editorialreview/view/'
        r'(?P<editorial_review_id>\d+)/$',
        editor_view_editorial_review,
        name='editor_view_editorial_review'
    ),
    url(  # Review.
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_id>\d+)/assignment/(?P<review_id>\d+)/$',
        editor_review_assignment,
        name='editor_review_assignment'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_id>\d+)/assignment/(?P<review_id>\d+)/hide/$',
        hide_review,
        name='hide_review'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/review/round/'
        r'(?P<round_id>\d+)/assignment/(?P<review_id>\d+)/set/due/$',
        update_review_due_date,
        name='update_review_due_date'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/files/'
        r'(?P<review_type>[-\w]+)/add/$',
        add_review_files,
        name='add_review_files'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/files/'
        r'(?P<file_id>\d+)/(?P<review_type>[-\w]+)/delete/$',
        delete_review_files,
        name='delete_review_files'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/reviewers/'
        r'(?P<review_type>[-\w]+)/add/(?P<round_number>\d+)/$',
        editor_add_reviewers,
        name='editor_add_reviewers'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/revisions/'
        r'(?P<revision_id>\d+)/due/$',
        editor_change_revision_due_date,
        name='editor_change_revision_due_date'
    ),
    url(
        r'^submission/submission/(?P<submission_id>\d+)/'
        r'revisions/request/returner/(?P<returner>[-\w]+)/$',
        request_revisions,
        name='request_revisions'
    ),
    url(
        r'^submission/submission/(?P<submission_id>\d+)/'
        r'revisions/view/(?P<revision_id>\d+)/$',
        editor_view_revisions,
        name='editor_view_revisions'
    ),
    url(  # Editing.
        r'^submission/(?P<submission_id>\d+)/editing/$',
        editor_editing,
        name='editor_editing'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/editing/assign/copyeditor/$',
        assign_copyeditor,
        name='assign_copyeditor'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/editing/view/'
        r'copyeditor/(?P<copyedit_id>\d+)/$',
        view_copyedit,
        name='view_copyedit'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/remove/'
        r'(?P<assignment_type>[-\w]+)/(?P<assignment_id>\d+)/$',
        remove_assignment_editor,
        name='remove_assignment_editor'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/editing/assign/indexer/$',
        assign_indexer,
        name='assign_indexer'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/editing/view/'
        r'indexer/(?P<index_id>\d+)/$',
        view_index,
        name='view_index'
    ),
    url(  # Production.
        r'^submission/(?P<submission_id>\d+)/publish/$',
        editor_publish,
        name='editor_publish'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/files/$',
        files_for_production,
        name='files_for_production'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/$',
        editor_production,
        name='editor_production'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/add/format/$',
        add_format,
        name='add_format'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/add/chapter/$',
        add_chapter,
        name='add_chapter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/chapter/'
        r'(?P<chapter_id>\d+)/view/$',
        view_chapter,
        name='editor_view_chapter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/chapter/'
        r'(?P<chapter_id>\d+)/add/format/$',
        add_chapter_format,
        name='add_chapter_format'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/chapter/'
        r'(?P<chapter_id>\d+)/update/$',
        update_chapter,
        name='editor_update_chapter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/chapter/'
        r'(?P<chapter_id>\d+)/view/format/(?P<format_id>\d+)/$',
        view_chapter_format,
        name='editor_view_chapter_format'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/add/physical/$',
        add_physical,
        name='add_physical'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/add/format/'
        r'(?P<file_id>\d+)/$',
        add_format,
        name='add_format_existing'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/add/chapter/'
        r'file/(?P<file_id>\d+)/$',
        add_chapter,
        name='add_chapter_existing'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/add/chapter/'
        r'(?P<chapter_id>\d+)/file/(?P<file_id>\d+)/$',
        add_chapter,
        name='add_chapter_existing_id'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/delete/'
        r'(?P<format_or_chapter>[-\w]+)/(?P<id>\d+)/$',
        delete_format_or_chapter,
        name='delete_format_or_chapter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/update/'
        r'(?P<format_or_chapter>[-\w]+)/(?P<id>\d+)/$',
        update_format_or_chapter,
        name='update_format_or_chapter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/assign/typesetter/$',
        assign_typesetter,
        name='assign_typesetter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/view/typesetter/'
        r'(?P<typeset_id>\d+)/$',
        view_typesetter,
        name='view_typesetter'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/view/typesetter/'
        r'(?P<typeset_id>\d+)/alter/due-date/$',
        view_typesetter_alter_due_date,
        name='view_typesetter_alter_due_date'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/view/typesetter/'
        r'(?P<typeset_id>\d+)/alter/author-due/$',
        view_typesetter_alter_author_due,
        name='view_typesetter_alter_author_due'
    ),

    url(
        r'^submission/(?P<submission_id>\d+)/production/chapter/'
        r'(?P<chapter_id>\d+)/add/author/$',
        add_edit_chapter_author,
        name='add_chapter_author'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/production/chapter/'
        r'(?P<chapter_id>\d+)/edit/author/(?P<chapter_author_id>\d+)/$',
        add_edit_chapter_author,
        name='edit_chapter_author'
    ),
    url(  # Catalog.
        r'^submission/(?P<submission_id>\d+)/catalog/$',
        catalog,
        name='catalog'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/marc21/$',
        catalog_marc21,
        name='catalog_marc21'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/marc21/load/'
        r'(?P<type>[-\w]+)$',
        catalog_marc21,
        name='catalog_marc21_load'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/identifiers/$',
        identifiers,
        name='identifiers'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/identifiers/'
        r'(?P<identifier_id>\d+)/$',
        identifiers,
        name='identifiers_with_id'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/retailers/$',
        retailers,
        name='retailers'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/retailers/'
        r'(?P<retailer_id>\d+)/$',
        retailers,
        name='retailer_with_id'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/contributor/'
        r'(?P<contributor_type>[-\w]+)/(?P<contributor_id>\d+)/$',
        update_contributor,
        name='update_contributor'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/contributor/'
        r'(?P<contributor_type>[-\w]+)/$',
        update_contributor,
        name='add_contributor'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/catalog/contributor/'
        r'(?P<contributor_type>[-\w]+)/(?P<contributor_id>\d+)/delete/$',
        delete_contributor,
        name='delete_contributor'
    ),
    url(  # Contract.
        r'^contract/(?P<submission_id>\d+)/manage/$',
        contract_manager,
        name='contract_manager'
    ),
    url(
        r'^contract/(?P<submission_id>\d+)/manage/(?P<contract_id>\d+)/$',
        contract_manager,
        name='contract_manager_edit'
    ),
    url(
        r'^submission/(?P<submission_id>\d+)/decline/$',
        decline_submission,
        name='editor_decline_submission'
    ),
    url(  # WORKFLOW New Submissions.
        r'^new/$',
        new_submissions,
        name='new_submissions'
    ),
    url(
        r'^new/submission/(?P<submission_id>\d+)/$',
        view_new_submission,
        name='view_new_submission'
    ),
]
