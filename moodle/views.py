from django.shortcuts import render, get_object_or_404, redirect
from . import models, forms

# Create your views here.
def homepage(request):
	courses = models.Course.objects.all()
	return render(request, 'homepage.html',{'courses':courses})

def course_view(request,pk):

	course = get_object_or_404(models.Course,pk=pk)
	regs=course.registrations.all()
	is_course_prof=False
	can_leave=False
	can_join=False
	if request.user.is_authenticated:
		for i in regs:
			if request.user==i.student:
				can_leave=True
		if request.user==course.prof:
			is_course_prof=True
		elif request.user.profile.is_prof==0:
			can_join= not can_leave

	can_see=False
	messages=[]
	for message in models.Message.objects.filter(course=course):
		regs=message.course.registrations.all()
		for i in regs:
			if request.user==i.student and i.date<=message.date:
				can_see=True
		if is_course_prof:
			can_see=True
		if can_see:
			messages.append(message)

	params= {
		'messages':messages, 
		'course':course, 
		'regs':regs, 
		'is_course_prof':is_course_prof, 
		'can_leave':can_leave, 
		'can_join':can_join,
		}

	return render(request, 'course.html',params)


def my_courses_view(request):
	
	if (request.user.is_authenticated):
		if request.user.profile.is_prof==1 :
			courses= request.user.courses_teaching.all()
			return render(request, 'homepage.html',{'courses':courses})
		else:
			courses=[]
			regs= request.user.registrations.all()
			for i in regs:
				courses.append(i.course)
			return render(request, 'homepage.html',{'courses':courses})
	return redirect('home')

def create_course_view(request):
	if request.user.is_authenticated and request.user.profile.is_prof==1 and request.method=='POST':
		form = forms.CourseForm(request.POST)
		if form.is_valid():
			course=form.save(commit=False)
			course.prof=request.user
			course.save()
			return redirect('course', pk=course.pk)
	else:
		form=forms.CourseForm()
	return render(request, 'create_course.html',{'form':form, 'can_create': request.user.profile.is_prof==1})	


def join_course_view(request, pk):
	course = get_object_or_404(models.Course,pk=pk)
	can_leave=False
	can_join=False
	regs=course.registrations.all()
	if request.user.is_authenticated:
		for i in regs:
			if request.user==i.student:
				can_leave=True
		if request.user.profile.is_prof==0:
			can_join= not can_leave
	if request.method == 'POST' and can_join:
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			reg=form.save(commit=False)
			reg.course=course
			reg.student=request.user
			reg.save()
			return redirect('course', pk=course.pk)
	else:
		form=forms.RegistrationForm()
	return render(request, 'join_course.html', {'form' : form, 'course' : course, 'can_join':can_join})
def leave_course_view(request,pk):
	course = get_object_or_404(models.Course,pk=pk)
	can_leave=False
	regs=course.registrations.all()
	if request.user.is_authenticated:
		for i in regs:
			if request.user==i.student:
				can_leave=True
				reg=i
	if request.method == 'POST' and can_leave:
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			reg.delete()
			return redirect('course', pk=course.pk)
	else:
		form=forms.RegistrationForm()
	return render(request, 'leave_course.html', {'form' : form, 'course' : course, 'can_leave': can_leave})

def new_topic(request):
    user=request.user
    object_list=Post.objects.all()
    if request.method == 'POST':
        form= NewPostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=user
            post.title=''
            post.save()
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'home.html', {'form' : form, 'object_list' : object_list})

def create_message_view(request,pk):
	course = get_object_or_404(models.Course,pk=pk)
	if request.user.is_authenticated and request.user==course.prof and request.method=='POST':
		form = forms.MessageForm(request.POST)
		if form.is_valid():
			message=form.save(commit=False)
			message.course=course
			message.save()
			return redirect('message', pk=message.pk)
	else:
		form=forms.MessageForm()
	return render(request, 'create_message.html',{'form':form, 'can_create': request.user==course.prof})	

def message_view(request,pk):

	message = get_object_or_404(models.Message,pk=pk)
	can_see=False
	if request.user.is_authenticated:
		regs=message.course.registrations.all()
		for i in regs:
			if request.user==i.student and i.date<=message.date:
				can_see=True
		if request.user==message.course.prof:
			can_see=True

	return render(request, 'message.html',{'message':message, 'can_see':can_see})
