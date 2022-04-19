# from django.http import HttpResponse
# from django.shortcuts import render
# # Create your views here.
# def post_get(request):
#     if 'query' in request.GET:
#         query = request.GET['query']
#         from thesaurus.tasks import run_sch
#         run_sch.delay()
#     elif 'eng' in request.GET:
#         post = request.GET['eng']
#         from findout.tasks import run_postfetch
#         run_postfetch.delay()
#         return HttpResponse('eng')
#     else:
#         pass
    
#     return HttpResponse('Done')