from django.test import TestCase
from app.models import Survey, Question, Answer
from django.contrib.auth.models import User
import unittest

# Create your tests here.
class UserModelTest(TestCase):
    #create a function to make a default user
    def create_user(self):
        self.subject = User.objects.create(username='testuser', email='testuser@django.com',password='testuser')
        return self.subject
#test the survey model and create a survey object
class SurveyModelTest(TestCase):
    def test_string_representation(self):
        survey = Survey(name='My Survey')
        self.assertEqual(str(survey), survey.name)
    #create a survey object
    def test_survey_creation(self):
        user = UserModelTest()
        survey = Survey.objects.create(name='My Survey',creator=user.create_user())
        self.assertTrue(isinstance(survey, Survey))
        self.assertEqual(survey.__str__(), survey.name)

#test the question model using the survey and create a question object
class QuestionModelTest(TestCase):
    def test_string_representation(self):
        question = Question(question_text='My Question')
        self.assertEqual(str(question), question.question_text)
    #create a question object
    def test_question_creation(self):
        user = UserModelTest()
        survey = Survey.objects.create(name='My Survey',creator=user.create_user())
        question = Question.objects.create(question_text='My Question', survey=survey)
        self.assertTrue(isinstance(question, Question))
        self.assertEqual(question.__str__(), question.question_text)

#test the answer model using the survey and question and create an answer object



#run the tests
if __name__ == '__main__':
    unittest.main()

def create_user():
    user = User.objects.create(username='testuser', email='test@django.com',password='testuser')
    return user

#create a survey object
def create_survey():
    user = create_user()
    survey = Survey.objects.create(name='My Survey',creator=user)
    return survey
create_survey()

