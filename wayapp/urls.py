from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    #path("todos/", views.todos, name="Todos"),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('profile_user', views.profile_user, name='profile_user'),
    path('affiliations', views.affiliations, name='affiliations'),    
    path('present_user', views.present_user, name='present_user'),  #login settings.py
    path('profile_employer', views.profile_employer, name='profile_employer'),
    path('create_profile', views.create_profile, name='create_profile'),
    path('update_profile', views.update_profile, name='update_profile'),    
    path('create_jobdescription', views.create_jobdescription, name='create_jobdescription'),
    path('create_jobdescription_another/<str:jd_id>/', views.create_jobdescription_another, name='create_jobdescription_another'),    
    path('update_jobdescription/<str:jd_id>/', views.update_jobdescription, name='update_jobdescription'),
    path('update_jobdescription_another/<str:jd_id>/', views.update_jobdescription_another, name='update_jobdescription_another'),
    #path('update_jobpost', views.update_jobpost, name='update_jobpost'),
    path('matched_results', views.matched_results, name='matched_results'),   #add user's id here
    path('matched_interns_results/<str:jd_id>/', views.matched_interns_results, name='matched_interns_results'),    
    #path('tokenization', views.tokenization, name='tokenization'),    
    path('register', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
