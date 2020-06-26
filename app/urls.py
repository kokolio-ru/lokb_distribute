"""app URL Configuration

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
from distr import views
from django.contrib.auth.decorators import login_required

handler404 = 'distr.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('modal/', views.modal),
    path('login/', views.Auth.as_view()),
    path('logout/', views.logout),

    path('patient/<int:patient_id>/', login_required(views.PatientView.as_view(), login_url='/login/'), name='edit_patient'),
    path('room/<int:room_id>/', views.get_room),
    path('room/distribution/', views.distribute_patient),
    path('position/<int:position_id>/comment/', views.save_position_comment),
    path('delete/<int:position_id>/', views.delete_patient)
]
