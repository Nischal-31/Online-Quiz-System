from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Quiz, Question, Choice, UserQuizAttempt, Category

def quiz_list(request):
    categories = Category.objects.all()
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'quiz/quiz_list.html', {
        'quizzes': quizzes,
        'categories': categories
    })

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.all()
    choices_data = []
    for question in questions:
        choices = question.choices.all()
        choices_data.append({
            'id': question.id,
            'text': question.text,
            'type': question.question_type,
            'choices': [{'id': c.id, 'text': c.text} for c in choices]
        })
    return render(request, 'quiz/quiz_start.html', {
        'quiz': quiz,
        'questions': choices_data
    })

@login_required
@csrf_exempt
def submit_quiz(request):
    if request.method == 'POST':
        data = request.POST
        quiz_id = data.get('quiz_id')
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        score = 0
        total_questions = quiz.questions.count()
        
        for question_id, answer_id in data.items():
            if question_id.isdigit():
                question = get_object_or_404(Question, id=question_id)
                try:
                    choice = Choice.objects.get(id=answer_id, question=question)
                    if choice.is_correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass
        
        percentage = (score / total_questions) * 100
        
        attempt = UserQuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            percentage=percentage
        )
        
        return JsonResponse({
            'success': True,
            'score': score,
            'total': total_questions,
            'percentage': round(percentage, 2)
        })
    
    return JsonResponse({'success': False})

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.user.is_authenticated:
        attempt = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).first()
    else:
        attempt = None
    return render(request, 'quiz/results.html', {
        'quiz': quiz,
        'attempt': attempt
    })