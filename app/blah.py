#import settings
import email
from django.conf import settings
from django.contrib.auth.models import User
from app.models import Survey, Question, Answer
#create a user
user = User.objects.create(username='testuser3',email='test3@django.com',password='testuser')
user = form.save()
#create a survey
survey = Survey.objects.create(name='My Survey',creator=user)
