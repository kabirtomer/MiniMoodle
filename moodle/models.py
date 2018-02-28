from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

COURSE_NAME_LENGTH=10
COURSE_SUBTITLE_LENGTH=100
MESSAGE_TITLE_LENGTH=100
# Create your models here.


class Course(models.Model):
    prof = models.ForeignKey('auth.User',on_delete=models.CASCADE, related_name="courses_teaching")
    name = models.CharField(max_length=COURSE_NAME_LENGTH)
    subtitle = models.CharField(max_length=COURSE_SUBTITLE_LENGTH, blank=True,  null=True)
    def __str__(self):
        return self.name


class Profile(models.Model):

    CHOICES=(
        (0, 'Student'),
        (1, 'Professor')
    )

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    is_prof = models.PositiveSmallIntegerField(choices=CHOICES,default=0)

    def __str__(self):
        return self.user.username + " profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Registration(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="registrations")
    student=models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="registrations")
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.student.username + " reg in " +self.course.name


class Message(models.Model):
    title=models.CharField(max_length=MESSAGE_TITLE_LENGTH)
    text=models.TextField()
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="messages")
    date=models.DateTimeField(default=timezone.now)





