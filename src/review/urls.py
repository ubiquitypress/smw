from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(
        r'dashboard/$',
        'review.views.reviewer_dashboard',
        name='reviewer_dashboard'
    ),
    url(  # Reviewer decision.
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision/$',
        'review.views.reviewer_decision',
        name='reviewer_decision_without'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision/(?P<decision>[-\w]+)/$',
        'review.views.reviewer_decision',
        name='reviewer_decision_with'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'decision/$',
        'review.views.reviewer_decision',
        name='reviewer_decision_without_access_key'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'decision/(?P<decision>[-\w]+)/$',
        'review.views.reviewer_decision',
        name='reviewer_decision_with_access_key'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/decision-email/'
        r'(?P<decision>accept|decline)/$',
        views.ReviewerDecisionEmail.as_view(),
        name='reviewer_decision_email'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/assignment/'
        r'(?P<review_assignment_id>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'decision-email/(?P<decision>accept|decline)/$',
        views.ReviewerDecisionEmail.as_view(),
        name='reviewer_decision_email_with_access_key'
    ),
    url(  # Review.
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/$',
        'review.views.review',
        name='review_with_access_key'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/$',
        'review.views.review',
        name='review_without_access_key'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/completion-email/$',
        views.ReviewCompletionEmail.as_view(),
        name='review_completion_email'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'completion-email/$',
        views.ReviewCompletionEmail.as_view(),
        name='review_completion_email_with_access_key'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/complete/$',
        'review.views.review_complete',
        name='review_complete'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/complete/$',
        'review.views.review_complete',
        name='review_complete_with_access_key'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/complete/no-redirect/$',
        'review.views.review_complete_no_redirect',
        name='review_complete_no_redirect'
    ),
    url(
        r'^(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/review-round/'
        r'(?P<review_round>\d+)/access_key/(?P<access_key>[-\w+]+)/'
        r'complete/no-redirect/$',
        'review.views.review_complete_no_redirect',
        name='review_complete_with_access_key_no_redirect'
    ),
    url(
        r'^review/review-request-declined/$',
        'review.views.review_request_declined',
        name='review_request_declined'
    ),
    url(  # Other.
        r'^download/(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/'
        r'assignment/(?P<review_id>\d+)/$',
        'review.views.generate_review_form',
        name='generate_review_form'
    ),
    url(
        r'^download/(?P<review_type>[-\w]+)/(?P<submission_id>\d+)/'
        r'assignment/(?P<review_id>\d+)/access_key/(?P<access_key>[-\w+]+)/$',
        'review.views.generate_review_form',
        name='generate_review_form_access_key'
    ),
)
