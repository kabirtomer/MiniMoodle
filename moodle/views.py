from django.shortcuts import render, get_object_or_404
from . import models

# Create your views here.
def homepage(request):
	courses = models.Course.objects.all()
	return render(request, 'homepage.html',{'courses':courses})

def course_view(request,pk):

	course = get_object_or_404(models.Course,pk=pk)
	regs=course.registrations.all()
	return render(request, 'course.html',{'course':course, 'regs':regs})
