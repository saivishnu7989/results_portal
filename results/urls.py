from django.urls import path

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_results, name='upload_results'),
    path('check/', views.check_result, name='result_check'),  # Student form
    path('result/', views.check_result, name='result_view'),    # Result display
    path('download/<str:roll_number>/<int:semester_id>/', views.download_pdf, name='download_pdf'),

    # urls.py
    path("check/<int:semester_id>/", views.check_result, name="check_result"),


    path('admin/login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', views.admin_logout, name='logout'),
    # path('admin/view-results/', views.view_all_results, name='view_all_results'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),
    path('refresh-captcha/', views.refresh_captcha, name='refresh_captcha'),
]