from django.urls import path
from .views import *

urlpatterns=[
	path('', homepage, name='home'),
	path('my_courses/', my_courses_view, name='my_courses'),
	path('course/<int:pk>/', course_view, name='course'),
	path('course/<int:pk>/leave_course/', leave_course_view, name='leave_course'),
	path('course/<int:pk>/join_course/', join_course_view, name='join_course'),
	path('create_course/', create_course_view, name='create_course'),
	path('course/<int:pk>/create_message/', create_message_view, name='create_message'),
	path('message/<int:pk>/', message_view, name='message'),
]