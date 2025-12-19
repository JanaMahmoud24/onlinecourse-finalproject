from django.shortcuts import render, get_object_or_404
from .models import Question, Submission, Choice, Learner

def submit(request):
    if request.method == "POST":
        # Example: get first learner (for simplicity)
        learner = Learner.objects.first()
        submission = Submission.objects.create(enrollment=learner)
        selected_choices = request.POST.getlist('choices')
        for choice_id in selected_choices:
            choice = Choice.objects.get(id=choice_id)
            submission.choices.add(choice)
        submission.save()
        return show_exam_result(request, submission.id)
    return render(request, "submit.html")

def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    total_questions = Question.objects.count()
    correct = 0
    for choice in submission.choices.all():
        if choice.is_correct:
            correct += 1
    score = int(correct / total_questions * 100) if total_questions else 0
    return render(request, "result.html", {"score": score, "submission": submission})
