from django.urls import path

from users import views

app_name = 'users'


urlpatterns = [
    path('', views.UsersList.as_view()),
    path('create/', views.UserRegisterView.as_view(), name='create'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('<user_id>/update', views.UserAccountView.as_view(), name='update'),
    path('<user_id>/delete', views.UserDeleteView.as_view(), name='delete')
]
