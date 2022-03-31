from django import forms
from django.forms import models
from app.models import Survey, Question, Answer

#a form for creating a new survey
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name']

#a form for creating a new question
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
#a form for creating a new answer
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
    
#a form to create a response
class ResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('answer')
        options = {(answer.id, answer.answer_text) for answer in question.answer_set.all()}
        super(ResponseForm, self).__init__(*args, **kwargs)
        #if the question type is SELECT make it a choice field
        if question.question_type == 'SELECT':
            self.fields['answer'] = forms.ChoiceField(choices=options)
        #if the question type is SELECT_MULTIPLE make it a multiple choice field
        elif question.question_type == 'SELECT_MULTIPLE':
            self.fields['answer'] = forms.MultipleChoiceField(choices=options)
        #if the question type is INTEGER make it a integer field
        elif question.question_type == 'INTEGER':
            self.fields['answer'] = forms.IntegerField()
        #if the question type is TEXT make it a text field
        else:
            self.fields['answer'] = forms.CharField()
#a base formset for creating responses
class BaseResponseFormSet(models.BaseFormSet):
    #get kwargs from answer index
    def get_kwargs(self, index):
        kwargs = super(BaseResponseFormSet, self).get_kwargs(index)
        kwargs['answer'] = self.data[index]['answer']
        return kwargs
