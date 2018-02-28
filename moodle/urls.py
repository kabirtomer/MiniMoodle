from django.urls import path
from .views import *

urlpatterns=[
	path('', homepage, name='home'),
	path('course/<int:pk>/', course_view, name='course'),
]