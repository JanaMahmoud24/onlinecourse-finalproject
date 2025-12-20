from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Submission

# Handles exam submission
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.create(user=request.user, course=course)
    for question in course.question_set.all():
        answer_id = request.POST.get(str(question.id))
        if answer_id:
            submission.choices.add(answer_id)
    submission.save()
    return show_exam_result(request, submission.id)

# Displays exam result
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    total = submission.course.question_set.count()
    correct = sum(1 for q in submission.course.question_set.all() if submission.is_correct(q))
    context = {
        'submission': submission,
        'score': int(correct / total * 100) if total > 0 else 0,
        'total': total,
        'correct': correct
    }
    return render(request, 'exam_result.html', context)
