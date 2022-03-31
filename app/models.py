from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from uuid import uuid4
from django.urls import reverse

# Create your models here.

class Survey(models.Model):
    ONE_PAGE = 0
    MULTIPLE_PAGES = 1

    DISPLAY =[
        (ONE_PAGE, 'One Page'),
        (MULTIPLE_PAGES, 'Multiple Pages'),
    ]
    #uuid field
    id = models.UUIDField(primary_key=True,default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    description = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    display_type = models.IntegerField(choices=DISPLAY, default=ONE_PAGE)
    redirect_url = models.URLField("Redirect URL", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #a meta class to set the singular and plural name
    class Meta:
        verbose_name_plural = "Surveys"
    def __str__(self):
        return self.name
    #a fuction to get the latest responses, if no responses are found it will return an empty list
    def get_latest_responses(self):
        return self.response_set.order_by('-updated_at')[:5]
    #a function to get the total number of responses
    def get_total_responses(self):
        return self.response_set.count()
    #a function get absolute url using the reverse function
    def get_absolute_url(self):
        return reverse('survey_detail', kwargs={'survey_slug': self.slug})
    #a function for the ONE_PAGE display type
    def get_one_page_display(self):
        return self.display_type == self.ONE_PAGE




#create a class for questions
class Question(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
		(TEXT, 'text'),
		(SELECT, 'select'),
		(SELECT_MULTIPLE, 'Select Multiple'),
		(INTEGER, 'integer'),
	)
    REQUIRED_CHOICES = 2
    REQUIRED_CHOICES_MULTI = 3

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    question_text = models.CharField(max_length=200)
    required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #a function that saves the questionif the question type is integer make the question_text an integer field:
    def save(self, *args, **kwargs):
        if self.question_type == Question.INTEGER:
            self.question_text = int(self.question_text)
        super(Question, self).save(*args, **kwargs)
    #a function that returns the question type
    def get_question_type(self):
        return self.question_type
    #a function that ruturn the total amout of choices
    def get_total_choices(self):
        return self.choice_set.count()
    #a function that make sure the question has at least 2 choices if the question type is select-multiple REQUIRED_CHOICES will be 3
    def clean(self, *args, **kwargs):
        count = self.get_total_choices
        if self.question_type == Question.SELECT_MULTIPLE:
            if count < self.REQUIRED_CHOICES_MULTI:
                raise ValidationError('A question must have at least 3 choices')
        else:
            if count < self.REQUIRED_CHOICES:
                raise ValidationError('A question must have at least 2 choices')


    

#create a class for answers
class Answer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text
    #a function to get the total number of responses
    def get_total_responses(self):
        return self.response_set.count()
#create a class for responses
class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    choice = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participant_key = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    answered_on = models.DateTimeField(auto_now_add=True)
#create a class for submissions
class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

