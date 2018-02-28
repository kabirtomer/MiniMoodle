from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
	class Meta:
		model=Registration
		fields=[]

class CourseForm(forms.ModelForm):
	class Meta:
		model=Course
		fields=['name', 'subtitle']

class MessageForm(forms.ModelForm):
	class Meta:
		model=Message
		fields=['title','text']