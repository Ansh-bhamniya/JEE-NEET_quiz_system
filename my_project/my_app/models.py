from django.db import models
from django.contrib.auth.models import User
import pandas as pd

# Create your models here.
class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE , null = True)
    email_address = models.CharField(max_length=55 , unique= True , null=True, verbose_name= 'E-mail')
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=15)
    class Meta:
        verbose_name_plural= 'Categories'
    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quiz_file = models.FileField(upload_to='quiz/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title        

    def save(self, *args, **kwargs):
        """Save the Quiz object and import questions from the uploaded Excel file."""
        super().save(*args, **kwargs)  # Save the quiz first
        if self.quiz_file:
            self.import_quiz_from_excel()  # Import questions after saving

    def import_quiz_from_excel(self):
        """Reads the Excel file and creates Question & Choice objects."""
        df = pd.read_excel(self.quiz_file.path)

        for index, row in df.iterrows():
            question_text = row.get('Question', '')  # Fetch question text
            choice1 = row.get('A', '')  # Fetch choices
            choice2 = row.get('B', '')
            choice3 = row.get('C', '')
            choice4 = row.get('D', '')
            correct_answer = row.get('Answer', '')

            # Create the Question object
            question = Question.objects.get_or_create(quiz=self, text=question_text)

            # Create Choice objects
            Choice.objects.get_or_create(question=question, text=choice1, is_correct=(correct_answer == 'A'))
            Choice.objects.get_or_create(question=question, text=choice2, is_correct=(correct_answer == 'B'))
            Choice.objects.get_or_create(question=question, text=choice3, is_correct=(correct_answer == 'C'))
            Choice.objects.create(question=question, text=choice4, is_correct=(correct_answer == 'D'))


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:50]}, {self.text[:20]}"

