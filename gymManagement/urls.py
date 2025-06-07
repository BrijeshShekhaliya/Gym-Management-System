"""
URL configuration for gymManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from accounts import views
from gym.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about',About,name="about"),
    path('contact',Contact,name="contact"),
    path('',Index,name="home"),
    path('admin_login',Admin_Login,name="admin_login"),
    path('logout',Logout_admin,name="logout"),

    path('add_equipment', Add_Equipment, name="add_equipment"),
    path('view_equipment', View_Equipment, name="view_equipment"),
    path('delete_equipment(?P<int:pid>)', Delete_Equipment, name="delete_equipment"),

    path('add_plan', Add_Plan, name="add_plan"),
    path('view_plan', View_Plan, name="view_plan"),
    path('delete_plan(?P<int:pid>)', Delete_Plan, name="delete_plan"),

    path('add_member', Add_Member, name="add_member"),
    path('view_member', View_Member, name="view_member"),
    path('delete_member(?P<int:pid>)', Delete_Member, name="delete_member"),

    path('add_request', Add_Request, name="add_request"),
    path('view_request', View_Request, name="view_request"),
    path('delete_request(?P<int:pid>)', Delete_Request, name="delete_request"),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Including the accounts app URLs
    path('', include('main.urls')),

    path('member_details/', view_member_details, name='member_details'),

    path('upload_video/',upload_video, name='upload_video'),
    path('view_videos/',view_videos, name='view_videos'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
