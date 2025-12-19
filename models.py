from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Instructor(models.Model):
    name = models.CharField(max_length=100)

class Learner(models.Model):
    name = models.CharField(max_length=100)

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    enrollment = models.ForeignKey(Learner, on_delete=models.CASCADE)  # required by LMS
    choices = models.ManyToManyField(Choice)

    def formatted_output(self):
        return f"Submission by {self.enrollment.name}: {self.choices.count()} choices selected"
