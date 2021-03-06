from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect, QueryDict
from django.views.generic import View

from auth import REDIRECT_FIELD_NAME


def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page.
    """
    resolved_url = login_url or settings.LOGIN_URL

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))


class AccessMixin:
    """
    Abstract CBV mixin that gives access mixins the same customizable
    functionality.
    """
    _login_url = None
    _permission_denied_message = ''
    _raise_exception = False
    _redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        """
        Override this method to override the login_url attribute.
        """
        login_url = self._login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self._permission_denied_message

    def get_redirect_field_name(self):
        """
        Override this method to override the redirect_field_name attribute.
        """
        return self._redirect_field_name

    def handle_no_permission(self):
        if self._raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class UserPassesTestMixin(View, AccessMixin):
    """
    Deny a request with a permission error if the test_func() method returns
    False.
    """

    def __init__(self, test_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._test_object = test_object

    def get_test_object(self):
        """
        Override this method to use a different test_func method.
        """
        return self._test_object

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_object().test(self)
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
