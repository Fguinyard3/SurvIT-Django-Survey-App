from django.contrib import admin

#import the survey, question, and answer models
from app.models import Survey, Question, Answer, Response, Submission


# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(Submission)

