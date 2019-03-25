import datetime
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_info = request.META.get('PATH_INFO')
        time_format = '%Y-%m-%d %H:%M:%S'
        last_login = request.session.get('last_login')
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.user.Active:
                print('middleware.... is ajax request ', request.is_ajax())
                print(path_info)
                print(path_info == '/fetch_request')
                current_datetime = datetime.datetime.now()
                if last_login:
                    last = (current_datetime - datetime.datetime.strptime(last_login,time_format)).seconds
                    print('last = ', last)
                    print('settings.SESSION_IDLE_TIMEOUT = ', settings.SESSION_IDLE_TIMEOUT)
                    if last > settings.SESSION_IDLE_TIMEOUT and not request.is_ajax():
                        logout(request)
                        # del request.session['last_login']
                        return HttpResponseRedirect(settings.LOGIN_URL)
                    elif not (path_info == '/fetch_request'):
                        request.session['last_login'] = datetime.datetime.strftime(current_datetime, time_format)

                else:
                    request.session['last_login'] = datetime.datetime.strftime(current_datetime,time_format)
                return response

        if path_info.startswith(settings.CONFIRM_RESET_PASSWORD):
            return response

        if not (path_info in [settings.LOGIN_URL, settings.FORGOT_PASSWORD_URL, settings.LOGIN_CHECK_URL, settings.RESET_PASSWORD]):
            return HttpResponseRedirect(settings.LOGIN_URL)

        return response
