from django.urls import path
from . import views

urlpatterns = [
    # Submit exam for a course
    path('course/<int:course_id>/submit/', views.submit, name='submit'),

    # Show exam result for a course
    path('course/<int:course_id>/result/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),
]
