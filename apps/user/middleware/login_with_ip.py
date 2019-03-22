import random
import string

from django.contrib.auth import login, get_user_model
from django.utils.deprecation import MiddlewareMixin


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            return None

        UserModel = get_user_model()
        ip = request.META['REMOTE_ADDR']
        try:
            user = UserModel.objects.get(ip=ip)
        except UserModel.DoesNotExist:
            username = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for x in range(10))
            user = UserModel.objects.create(ip=ip, username=username)
        login(request, user)
        return None
