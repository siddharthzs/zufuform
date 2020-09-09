"""dynamic_form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from home.views import home, blank_form, blankform_save, view_allform, detailform, form_reponse, viewreponse, thankyou, formremove
import users.views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='web-home'),
    path('form/new/',blank_form,name='web-blank'),
    path('form/viewall/',view_allform,name='web-viewall'),
    path('form/<slug>/detail/',detailform,name='web-detail'),
    path('form/save/',blankform_save,name='web-blankform-save'),
    path('form/user/<slug>/response/',form_reponse,name='web-form-response'),
    path('form/<slug>/responses/',viewreponse,name='web-view-response'),
    path('form/<slug>/delete/',formremove,name='web-delete-form'),
    path('form/<slug>/responses/thankyou/',thankyou,name='web-thankyou'),
    # Authentication Views
    path('user/register/', users_views.register, name='web-register'),
    path('user/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='web-login'),
    path('user/logout/', auth_views.LogoutView.as_view(next_page='/user/login/',extra_context={'message':'You have been logged out!'}), name='web-logout'),
]
