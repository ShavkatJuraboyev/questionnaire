from django.db import models
from django.contrib.auth.models import User
from users.models import Role

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_roles = models.ManyToManyField(Role)  # Kimlar uchun
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[
        ('text', 'Matn'),
        ('radio', 'Bitta javob'),
        ('checkbox', 'Bir nechta javob'),
        ('rating', 'Baholash')
    ])

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.text

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)
    text_answer = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Javob: {self.user.username} - {self.question}"
