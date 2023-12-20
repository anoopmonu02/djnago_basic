"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from home.views import *

urlpatterns = [
    path('',home),
    path('about/',about,name='about'),
    path('login/',login_page,name='login_page'),
    path('logout/',logout_page,name='logout_page'),

    #path('query/', ormMethodSample, name='query'),
    path('query/', ormMethodSample1, name='query'),

    path('register/',register,name='register'),
    path('contact/',contact,name='contact'),
    path('delete_contact/<id>/',delete_contact,name='delete_contact'),
    path('update_contact/<id>/',update_contact,name='update_contact'),
    path("contacts/", contacts,name='contact_list'),

    path('students/', get_student_data, name='get_student_data'),
    path('see_stu_marks/<student_id>/',see_marks, name='see_marks'),

    path('send_email/', send_email, name='send_email'),

    path('admin/', admin.site.urls),
]
