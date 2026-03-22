from django.contrib import admin
from .models import Category, Quiz, Question, Choice, UserQuizAttempt


# 🔹 Inline: Choices inside Question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


# 🔹 Inline: Questions inside Quiz
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


# 🔹 Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


# 🔹 Quiz Admin
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title',)
    inlines = [QuestionInline]


# 🔹 Question Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question_type', 'created_at')
    list_filter = ('question_type', 'quiz')
    search_fields = ('text',)
    inlines = [ChoiceInline]


# 🔹 Choice Admin
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)


# 🔹 User Quiz Attempt Admin
@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'quiz', 'score', 'total_questions', 'percentage', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user__username', 'quiz__title')