from pathlib import Path
import urllib.parse
from django.http import Http404
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.conf import settings
from .forms import UploadFileForm
from PIL import Image


if hasattr(settings, 'IMAGE_UPLOADER_MAX_FILE_SIZE'):
    max_size = settings.IMAGE_UPLOADER_MAX_FILE_SIZE
else:
    max_size = 5011000
    # pass

class NoImageException(Exception):
    pass


def get_storage_class():
    if hasattr(settings, 'IMAGE_UPLOADER_FILE_STORAGE'):
        return import_string(settings.IMAGE_UPLOADER_FILE_STORAGE)
    return import_string(settings.DEFAULT_FILE_STORAGE)


storage = get_storage_class()


def image_verify(f):
    try:
        size = len((Image.open(f)).fp.read())
        if size < max_size:
            Image.open(f).verify()
        else:
            raise NoImageException
        
    except IOError:
        raise NoImageException


def handle_uploaded_file(f):
    folder = getattr(settings, 'IMAGE_UPLOADER_UPLOADS_FOLDER', 'my_uploader')
    uploads_path = Path(settings.MEDIA_ROOT, folder)
    fs = storage(location=uploads_path)
    filename = fs.save(f.name, f)
    return '/'.join([urllib.parse.urljoin(fs.base_url, folder), filename])


def upload_file(request):
    if request.method == 'POST' and request.user.is_active:
        form = UploadFileForm(request.POST, request.FILES)
        try:
            image_verify(request.FILES['upload'])
        except NoImageException as ex:
            return JsonResponse({
                "error": {
                    "message": "File size is greater than {} {} bytes".format(str(ex), max_size)
                }
            })
        if form.is_valid():
            url = handle_uploaded_file(request.FILES['upload'])
            return JsonResponse({'url': url})
    raise Http404(_('Page not found.'))
