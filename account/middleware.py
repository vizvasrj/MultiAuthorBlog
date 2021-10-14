from django.http import response
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

def subdomain_course_middleware(get_reaponse):
    """
    Subdomain form username
    """
    def middleware(request):
        host_parts = request.get_host().split('.')
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # get username for the given subdomain
            user = get_object_or_404(User, username=host_parts[0])
            user_url = reverse(
                'user_detail',
                args=[user.username]
            )
            # redirect current request to the user_detail view
            url = '{}://{}{}'.format(
                request.scheme,
                '.'.join(host_parts[1:]),
                user_url
            )
            return redirect(url)
        response = get_reaponse(request)
        return response
    return middleware