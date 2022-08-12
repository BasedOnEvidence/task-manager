"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from users import views as user_view
from statuses import views as status_view
from django.urls import path

urlpatterns = [
    path('', user_view.UsersList.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', user_view.UsersList.as_view(), name='users'),
    path('login/', user_view.UserAuthenticationView.as_view(), name='login'),
    path('users/logout/', user_view.UserLogoutView.as_view(), name='logout'),
    path('users/create/', user_view.UserRegisterView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', user_view.UserAccountView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', user_view.UserDeleteView.as_view(), name='delete_user'),
    path('statuses/', status_view.StatusesListView.as_view(), name='statuses'),
    path('statuses/create/', status_view.StatusCreateView.as_view(), name='create_status'),
    path('statuses/<int:pk>/update/', status_view.StatusChangeView.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', status_view.StatusDeleteView.as_view(), name='delete_status'),
]
