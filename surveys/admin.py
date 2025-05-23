from django.contrib import admin
from django.contrib import admin
from .models import Survey, Question, Option, Answer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ['text', 'survey', 'question_type']

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
