"""DoubtsSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from Doubts import views
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'Doubts.views.error_404'
handler500 = 'Doubts.views.error_500'
handler403 = 'Doubts.views.error_403'
handler400 = 'Doubts.views.error_400'

urlpatterns = [
    path('admin', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login', views.login),
    path('add_question/', views.new_question),
    path('register_t/', views.register_t),
    path('login_t', views.login_t),
    path('answer/', views.answer),
    path('teacher_home', views.teacher_home),
    path('student_home', views.student_home),
    path('view_answer/', views.view_answer),
    url(r'^$', views.home_r, name="home"),
    path('home', views.home),
    path('profile', views.profile),
    path('profile_t', views.profile_t),
    path('update_img', views.update_img),
    path('all_questions', views.all_questions),
    path('logout', views.logout),
    path('update_info', views.update_info),
    path('update_pass', views.update_pass),
    path('forget_pass', views.forget_pass),
    path('about_us', views.about_us),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
