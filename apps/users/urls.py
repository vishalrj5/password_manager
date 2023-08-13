from django.contrib import admin
from django.urls import path

from apps.users.views import DestroyUsersRecordsView, LoadUsersDatatable, UserCreateOrUpdateView, UsersView

app_name = 'users'

urlpatterns = [
    
    path('',UsersView.as_view(), name='users.index'),
    path('create',UserCreateOrUpdateView.as_view(), name='users.create'),
    path('<int:id>/update/', UserCreateOrUpdateView.as_view(), name='users.update'),
    path('load_users_datatable', LoadUsersDatatable.as_view(), name='load.users.datatable'),
    path('destroy_records/', DestroyUsersRecordsView.as_view(), name='users.records.destroy'),
    
    
    
]
