from django.conf.urls import url
from django.urls import path

from . import views


# urlpatterns = [
#     path('upload_file/', views.upload_file, name='upload-file')
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.customProfileView.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/show_papers_stats/', views.customProfileView.show_papers_stats, name='show_papers_stats'),
    path('login/new_project', views.customProfileView.new_project, name='new_project'),
    path('login/select_project', views.customProfileView.select_project, name='select_project'),
    path('login/upload_file', views.customProfileView.upload_file, name='upload_file'),
    path('login/update_selected_project/', views.customProfileView.update_selected_project, name='update_selected_project'),
    path('login/update_papers_stats/', views.customProfileView.update_papers_stats, name='update_papers_stats'),
    path('login/apply_leiden_algorithm/', views.customProfileView.apply_leiden_algorithm, name='apply_leiden_algorithm'),
    path('login/show_graph/', views.customProfileView.show_graph, name='show_graph'),
    path('login/delete_project/', views.customProfileView.delete_project, name='delete_project')




]
