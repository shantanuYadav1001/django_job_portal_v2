from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.homeView, name='home'),

    path('signup/', views.SignupView.as_view(), name='applicant_register'),
    path('login/', views.LoginView.as_view(), name='applicant_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('job/add', views.post_job, name='job_post'),
    #path('employer_login/', views.EmployerLoginView.as_view(), name='employer_login'),
    path('logout/', views.sign_out, name='logout'),
    path('job_list/', views.job_list, name='joblist'),

    path('search/', views.job_search, name='job_search'),

    path('job/<int:job_id>/details', views.job_details, name='job_details'),
    path('job/<int:job_id>/apply', views.job_apply, name='apply'),
    path('my_applications/', views.my_applied_jobs, name='my_applications'),

    path('employer/job_list/', views.employer_job_list, name='employer_job_list'),
    path('employer/job_list/edit/<int:job_id>', views.edit_job, name='edit_job'),

    path('job_applications/<int:job_id>/', views.view_job_applications, name='job_applications'),
    path('job_applications/detail/<int:application_id>/', views.application_detail_view, name='application_detail'),
  
]
