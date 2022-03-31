from urllib import response
from django.http import Http404
from django.shortcuts import render , redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.urls import reverse
from .models import Survey, Question, Response, Answer
from .forms import SurveyForm, QuestionForm, AnswerForm, ResponseForm, BaseResponseFormSet
from django.db import transaction

#a function for a user to display their surveys
@login_required
#a function for a user to display their surveys
def survey_list(request):
    surveys = get_list_or_404(Survey, creator=request.user).order_by('-created_at')
    return render(request, 'surveys/survey_list.html', {'surveys': surveys})

#a function for a user to display thier survey
# only if the survey is active
@login_required
def survey_detail(request, survey_slug ,pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user, is_active=True)
    questions = survey.question_set.order_by('order')
    #get the total number of answers
    total_answers = 0
    for question in questions:
        total_answers += question.answer_set.count()
    
    host = request.get_host()
    path = reverse('survey_detail', kwargs={'survey_slug': survey_slug, 'pk': pk})
    url = f"{request.scheme}://{host}{path}"
    responses = Response.objects.filter(survey=survey).count()
    return render(request, 'surveys/survey_detail.html', {'survey': survey, 'questions': questions, 'responses': responses, 'url': url})

#a function for a user to create a survey
@login_required
def survey_create(request):
    if request.method == 'POST':
        survey_form = SurveyForm(request.POST)
        if survey_form.is_valid():
            survey = survey_form.save(commit=False)
            survey.creator = request.user
            survey.save()
            return redirect('survey_list', pk=survey.id)
    else:
        survey_form = SurveyForm()
    return render(request, 'surveys/survey_create.html', {'survey_form': survey_form})

#a function for a user to delete a survey
@login_required
def survey_delete(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user)
    survey.delete()
    return redirect('survey_list')
#a function for a user to edit a survey
@login_required
def survey_edit(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user)
    if request.method == 'POST':
        survey_form = SurveyForm(request.POST, instance=survey)
        if survey_form.is_valid():
            survey = survey_form.save(commit=False)
            survey.creator = request.user
            survey.save()
            return redirect('survey_list', pk=survey.id)
    else:
        survey_form = SurveyForm(instance=survey)
    return render(request, 'surveys/survey_edit.html', {'survey_form': survey_form})
#a function for a user to make the survey active
@login_required
def survey_activate(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user)
    survey.is_active = True
    survey.save()
    return redirect('survey_list')
#a function for a user to make the survey inactive
@login_required
def survey_deactivate(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user)
    survey.is_active = False
    survey.save()
    return redirect('survey_list')
#a function for a user to create a question
@login_required
def question_create(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('survey_detail', survey_slug=survey_slug, pk=pk)
    else:
        question_form = QuestionForm()
    return render(request, 'surveys/question_create.html', {'question_form': question_form})
#a function for a user to delete a question
@login_required
def question_delete(request, survey_slug, pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk, survey__pk=pk, survey__slug=survey_slug, survey__creator=request.user)
    question.delete()
    return redirect('survey_detail', survey_slug=survey_slug, pk=pk)
#a function for a user to edit a question
@login_required
def question_edit(request, survey_slug, pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk, survey__pk=pk, survey__slug=survey_slug, survey__creator=request.user)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect('survey_detail', survey_slug=survey_slug, pk=pk)
    else:
        question_form = QuestionForm(instance=question)
    return render(request, 'surveys/question_edit.html', {'question_form': question_form})
#a function for a user to create an answer
@login_required
def answer_create(request, survey_slug, pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk, survey__pk=pk, survey__slug=survey_slug, survey__creator=request.user)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('survey_detail', survey_slug=survey_slug, pk=pk)
    else:
        answer_form = AnswerForm()
    return render(request, 'surveys/answer_create.html', {'answer_form': answer_form})
#a function for a user to delete an answer
@login_required
def answer_delete(request, survey_slug, pk, question_pk, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk, question__pk=question_pk, question__survey__pk=pk, question__survey__slug=survey_slug, question__survey__creator=request.user)
    answer.delete()
    return redirect('survey_detail', survey_slug=survey_slug, pk=pk)
#a function for a user to edit an answer
@login_required
def answer_edit(request, survey_slug, pk, question_pk, answer_pk):
    answer = get_object_or_404(Answer, pk=answer_pk, question__pk=question_pk, question__survey__pk=pk, question__survey__slug=survey_slug, question__survey__creator=request.user)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST, instance=answer)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('survey_detail', survey_slug=survey_slug, pk=pk)
    else:
        answer_form = AnswerForm(instance=answer)
    return render(request, 'surveys/answer_edit.html', {'answer_form': answer_form})
#a function to complete a survey
def survey_start(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug)
    if request.method == 'POST':
        res = Response.objects.create(survey=survey)
        #redirect to the survey_complete page
        return redirect('survey_complete', survey_slug=survey_slug, pk=pk)
    return render(request, 'surveys/survey_start.html', {'survey': survey})
#a function to complete a survey
def survey_complete(request, survey_slug, pk, child_pk):
    #try to prefetch the questions and answers
    try:
        survey = Survey.objects.prefetch_related('questions__answers').get(pk=pk, slug=survey_slug, is_active=True)
    except Survey.DoesNotExist:
        raise Http404("Survey does not exist")
    #try to get the response
    try:
        res = Response.objects.get(survey=survey, pk=child_pk, complete=False)
    except Response.DoesNotExist:
        raise Http404("Response does not exist")
    #set all the questions
    questions = survey.questions.all()
    #set all the answers
    answers = []
    for question in questions:
        answers.append(question.answers.all())
    #get the kwargs for the form
    kwargs = {'answers': answers}
    #create a response formset
    ResponseFormSet = formset_factory(ResponseForm, formset=BaseResponseFormSet, max_num=len(questions))
    #if the request is a post
    if request.method == 'POST':
        #create the formset
        formset = ResponseFormSet(request.POST, kwargs=kwargs)
        #if the formset is valid
        if formset.is_valid():
            #use atomic to ensure the database is not changed if there is an error
            with transaction.atomic():
                for i in formset:
                    #create a response object
                    Response.objects.create(question=i.cleaned_data['question'], answer=i.cleaned_data['answer'], response_id=child_pk)
                #set the response to complete
                res.complete = True
                res.save()
            return redirect('survey_complete', survey_slug=survey_slug, pk=pk)
    else:
        #create the formset
        formset = ResponseFormSet(kwargs=kwargs)
    questions = zip(questions, formset)
    return render(request, 'surveys/survey_complete.html', {'questions': questions, 'survey': survey, 'child_pk': child_pk})    
#a function to tell the survey taker thank you for taking the survey
def survey_thank_you(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, is_active=True)
    return render(request, 'surveys/survey_thank_you.html', {'survey': survey})

# a function for a user to view all responses to a survey
@login_required
def survey_responses(request, survey_slug, pk):
    survey = get_object_or_404(Survey, pk=pk, slug=survey_slug, creator=request.user)
    responses = survey.responses.all()
    return render(request, 'surveys/survey_responses.html', {'survey': survey, 'responses': responses})