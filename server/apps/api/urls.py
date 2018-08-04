from rest_auth.views import LoginView, LogoutView, PasswordChangeView, \
    PasswordResetConfirmView, PasswordResetView, UserDetailsView

from django.conf.urls import include, url

from .swagger import get_swagger_view

urlpatterns = [

    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),

    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),

    url(r'^login/$', LoginView.as_view(), name='rest_login'),

    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),

    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),

    url(r'^register/', include('server.apps.tenants.registration.urls')),

    url(r'^me/$', UserDetailsView.as_view(), name='rest_user_details'),

    url(r'^users/', include('server.apps.accounts.urls', namespace='users')),

    url(r'^docs/$',
        get_swagger_view(title='Project API Documentaion'), name='api_docs'),

]
