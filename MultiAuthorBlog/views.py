from django.http import HttpResponse

def read_file(request):
    f = open('7263713672163767218367687767.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")