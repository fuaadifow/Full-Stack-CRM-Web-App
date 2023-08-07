# crm/models.py

import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    # Add other fields as needed

    def __str__(self):
        return self.name

class QuizQuestion(models.Model):
    question = models.CharField(max_length=255)

    def get_options(self):
        return self.quizanswer_set.values_list('answer_text', flat=True)

    def get_correct_answer(self):
        correct_answer = self.quizanswer_set.filter(is_correct=True).first()
        return correct_answer.answer_text if correct_answer else None

    def __str__(self):
        return self.question

class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username} - Score: {self.score}"

class Document(models.Model):
    document_type_choices = [
        ('invoice', 'Invoice'),
        ('certificate', 'Certificate'),
        ('sales_receipt', 'Sales Receipt'),
        ('contract', 'Contract'),
        ('others', 'Others'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=document_type_choices, default='invoice')
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    id_number = models.PositiveIntegerField(default=1)  # Use PositiveIntegerField for custom primary key

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Remove the file from the server before deleting the record
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check if the document is being created (not updated)
        if not self.pk:
            # Calculate the next available id_number for the current user
            last_document = Document.objects.filter(user=self.user).order_by('-id_number').first()
            if last_document:
                self.id_number = last_document.id_number + 1
            else:
                self.id_number = 1

        super().save(*args, **kwargs)


## Superuser 
# Username Is admin
# Password Is admin123