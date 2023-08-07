from django.contrib import admin
from .models import QuizQuestion, QuizAnswer, Certificate

admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(Certificate)
