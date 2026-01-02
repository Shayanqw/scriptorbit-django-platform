from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('publication/', views.publication, name='publication'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('blog/', views.blog, name='blog'),

    # path('login/', views.login_view, name='login'),
    # path('preview/', views.preview_view, name='preview'),
    # path('logout/', views.logout_view, name='logout'),


    # Default preview: if the URL is just /preview/, page defaults to "index.html"
    path('preview/', views.preview_view, name='preview_default'),
    # Catch-all for additional pages like /preview/menu.html, /preview/contact.html, etc.
    path('preview/<path:page>/', views.preview_view, name='preview_dynamic'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
	path('jobs', views.job_list, name='job_list'),
    path('apply/<slug:slug>/', views.job_apply, name='job_apply'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
