from django.db import models

COURSE_NAME_LENGTH=10
COURSE_SUBTITLE_LENGTH=100
# Create your models here.

class Course(models.Model):
	prof = models.ForeignKey('auth.User',on_delete=models.CASCADE, related_name="prof")
	name = models.CharField(max_length=COURSE_NAME_LENGTH)
	subtitle = models.CharField(max_length=COURSE_SUBTITLE_LENGTH, blank=True,  null=True)
	start_date=models.DateTimeField(blank=True, null=True)
	message= models.TextField(blank=True, null=True)
	students = models.ManyToManyField('auth.User', related_name='students')

	def __str__(self):
		return self.name





