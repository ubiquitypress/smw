from django.conf.urls import patterns, url


urlpatterns = patterns(
   '',
   url(
        r'(?P<submission_type>[-\w]+)/(?P<submission_id>\d+)/add/$',
        'editorialreview.views.add_editorial_review',
        name='add_editorial_review'
   ),
   url(
        r'download/(?P<file_id>\d+)/review/(?P<review_id>\d+)/editor/$',
        'editorialreview.views.download_editor_er_file',
        name='download_editor_er_file'
   ),
   url(
        r'download/(?P<file_id>\d+)/review/(?P<review_id>\d+)/$',
        'editorialreview.views.download_er_file',
        name='download_er_file'
   ),
   url(
        r'editor/view/(?P<review_id>\d+)/$',
        'editorialreview.views.view_editorial_review',
        name='view_editorial_review'
   ),
   url(
        r'remove/(?P<review_id>\d+)/$',
        'editorialreview.views.remove_editorial_review',
        name='remove_editorial_review'
   ),
   url(
        r'withdraw/(?P<review_id>\d+)/$',
        'editorialreview.views.withdraw_editorial_review',
        name='withdraw_editorial_review'
   ),
   url(
        r'update_due_date/(?P<review_id>\d+)/$',
        'editorialreview.views.update_editorial_review_due_date',
        name='update_editorial_review_due_date'
   ),
   url(
        r'review/(?P<review_id>\d+)/view_review/'
        r'(?P<non_editorial_review_id>\d+)/$',
        'editorialreview.views.view_non_editorial_review',
        name='view_non_editorial_review'
   ),
   url(
        r'review/(?P<review_id>\d+)/summary/$',
        'editorialreview.views.view_content_summary',
        name='view_content_summary'
   ),
   url(
        r'review/(?P<review_id>\d+)/thanks/$',
        'editorialreview.views.editorial_review_thanks',
        name='editorial_review_thanks'
   ),
   url(
        r'review/(?P<review_id>\d+)/$',
        'editorialreview.views.editorial_review',
        name='editorial_review'
   ),
   url(
        r'(?P<review_id>\d+)/email/$',
        'editorialreview.views.email_editorial_review',
        name='email_editorial_review'
   ),
   url(
        r'(?P<review_id>\d+)/email/editor/$',
        'editorialreview.views.editorial_reviewer_email_editor',
        name='editorial_reviewer_email_editor_not_logged_in'
   ),
   url(
        r'(?P<review_id>\d+)/email/editor/(?P<user_id>\d+)/$',
        'editorialreview.views.editorial_reviewer_email_editor',
        name='editorial_reviewer_email_editor_logged_in'
   )
)
