from django.urls import path

from users import views

app_name = 'users'


urlpatterns = [
    path('', views.UsersList.as_view(), name='users'),
    path('create/', views.UserRegisterView.as_view(), name='create'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('<int:pk>/update', views.UserAccountView.as_view(), name='update'),
    path('<int:pk>/delete', views.UserDeleteView.as_view(), name='delete')
]
