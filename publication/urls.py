from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.publication_create_view, name='publication_create'),
    path('list/', views.publication_list_view, name='publication_list'),
    path('detail/<slug:slug>/', views.publication_detail_view, name='publication_detail'),

    # publication fallow
    path('fallow/', views.publication_follow, name='publication_follow'),

    # my publication as editor
    path('addedby/', views.editor_as_my_publication, name='editor_as_my_publication'),
    path('myy/', views.admin_as_my_publication, name='admin_as_my_publication'),

    path('my/', views.my_publication_list, name='my_publication_list'),
    path('leave/', views.publication_leave, name='publication_leave'),

    path('mange/<int:pk>', views.manage_publication, name='manage_publication'),
]