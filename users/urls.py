from django.urls import path

from users import views


urlpatterns = [
    path('', views.UsersList.as_view()),
    path('create/', views.UserRegisterView.as_view(), name='create'),
    path('logout/', views.UserLogoutView.as_view(), name='logout')
]
