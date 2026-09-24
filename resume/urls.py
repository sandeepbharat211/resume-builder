from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Footer info pages
    path('about/', views.about_page, name='about'),
    path('help/', views.help_page, name='help'),
    path('contact/', views.contact_page, name='contact'),

    # Template
    path('choose-template/', views.choose_template, name='choose_template'),

    # Resume
    path('create/', views.create_resume, name='create_resume'),
    path('list/', views.resume_list, name='resume_list'),
    path('resume/<int:id>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:id>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<int:id>/preview/', views.preview_resume, name='preview_resume'),
    path('resume/<int:id>/pdf/', views.download_resume, name='download_resume'),
    path('resume/<int:id>/change-template/', views.change_template, name='change_template'),

    # Sections
    path('resume/<int:id>/education/add/', views.add_education, name='add_education'),
    path('education/<int:id>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:id>/delete/', views.delete_education, name='delete_education'),

    path('resume/<int:id>/experience/add/', views.add_experience, name='add_experience'),
    path('experience/<int:id>/edit/', views.edit_experience, name='edit_experience'),
    path('experience/<int:id>/delete/', views.delete_experience, name='delete_experience'),

    path('resume/<int:id>/project/add/', views.add_project, name='add_project'),
    path('project/<int:id>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:id>/delete/', views.delete_project, name='delete_project'),

    path('resume/<int:id>/skill/add/', views.add_skill, name='add_skill'),
    path('skill/<int:id>/delete/', views.delete_skill, name='delete_skill'),

    path('resume/<int:id>/certificate/add/', views.add_certificate, name='add_certificate'),
    path('certificate/<int:id>/delete/', views.delete_certificate, name='delete_certificate'),

    path('resume/<int:id>/language/add/', views.add_language, name='add_language'),
    path('language/<int:id>/delete/', views.delete_language, name='delete_language'),

    path('resume/<int:id>/hobby/add/', views.add_hobby, name='add_hobby'),
    path('hobby/<int:id>/delete/', views.delete_hobby, name='delete_hobby'),

    # AI
    path('resume/<int:id>/ai/', views.ai_assistant, name='ai_assistant'),
    path('resume/<int:id>/ai/generate/', views.ai_generate_text, name='ai_generate_text'),
    path('resume/<int:id>/ai/save/', views.ai_save_text, name='ai_save_text'),

    # Custom Admin
    path('myadmin/', views.admin_dashboard, name='admin_dashboard'),
    path('myadmin/users/', views.admin_users, name='admin_users'),
    path('myadmin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('myadmin/users/<int:user_id>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
    path('myadmin/resumes/', views.admin_resumes, name='admin_resumes'),
    path('myadmin/realtime/', views.admin_realtime, name='admin_realtime'),
]
