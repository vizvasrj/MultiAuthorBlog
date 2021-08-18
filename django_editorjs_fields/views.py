import os
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .config import (IMAGE_NAME, IMAGE_NAME_ORIGINAL, IMAGE_UPLOAD_PATH,
                     IMAGE_UPLOAD_PATH_DATE)
from .utils import storage


class ImageUploadView(View):
    http_method_names = ["post", "delete"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return JsonResponse(
                    {'success': 0, 'message': 'You can only upload images.'}
                )

            filename, extension = os.path.splitext(the_file.name)

            if IMAGE_NAME_ORIGINAL is False:
                filename = IMAGE_NAME(filename=filename, file=the_file)

            filename += extension

            upload_path = IMAGE_UPLOAD_PATH

            if IMAGE_UPLOAD_PATH_DATE:
                upload_path += datetime.now().strftime(IMAGE_UPLOAD_PATH_DATE)

            path = storage.save(
                os.path.join(upload_path, filename), the_file
            )
            link = storage.url(path)

            return JsonResponse({'success': 1, 'file': {"url": link}})
        return JsonResponse({'success': 0})

    def delete(self, request):
        path_file = request.GET.get('pathFile')

        if not path_file:
            return JsonResponse({'success': 0, 'message': 'Parameter "pathFile" Not Found'})

        base_dir = getattr(settings, "BASE_DIR", '')
        path_file = f'{base_dir}{path_file}'

        if not os.path.isfile(path_file):
            return JsonResponse({'success': 0, 'message': 'File Not Found'})

        os.remove(path_file)

        return JsonResponse({'success': 1})
