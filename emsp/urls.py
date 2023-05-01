"""newtask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from emsa import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('emp', views.emp),
    path('show/',views.employee_list),
    path('mshow/',views.manager_list),
    # path('edit_employee/<int:pk>/', views.edit_employee, name='update_employee'),
    path('update/<int:pk>', views.update_employee),
    path('delete/<int:pk>',views.delete_employee),
    path('search/',views.search),
    path('download/', views.download_page, name='download_page'),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('elogin/',views.EmployeeLogin,name='elogin'),
    path('updatep/',views.UpdatePassword,name='updatep'),
    path('fun/',views.fun),
    path('excp/',views.excp),
]
