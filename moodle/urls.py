from django.urls import path
from .views import *

urlpatterns=[
	path('', homepage, name='home'),
	path('my_courses/', my_courses_view, name='my_courses'),
	path('course/<int:pk>/', course_view, name='course'),
	path('course/<int:pk>/leave_course', leave_course_view, name='leave_course'),
	path('course/<int:pk>/join_course', join_course_view, name='join_course'),
]