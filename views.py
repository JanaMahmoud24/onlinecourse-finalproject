from django.shortcuts import render, redirect
from .models import Course, Choice, Submission, Question


def submit(request, course_id):
    course = Course.objects.get(id=course_id)
    submission = Submission.objects.create(
        user=request.user,
        course=course
    )

    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith('choice'):
            selected_choices.append(int(value))

    submission.choices.set(selected_choices)
    return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    submission = Submission.objects.get(id=submission_id)
    selected_ids = submission.choices.values_list('id', flat=True)

    score = 0
    total = 0
    for question in Question.objects.filter(lesson__course_id=course_id):
        total += question.grade
        if question.is_correct(selected_ids):
            score += question.grade

    passed = score >= (total * 0.7)

    return render(request, 'exam_result.html', {
        'course': submission.course,
        'score': score,
        'total': total,
        'passed': passed,
        'choices': selected_ids
    })
