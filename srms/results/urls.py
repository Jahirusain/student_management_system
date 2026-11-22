from django.urls import path
from .views import (
    student_result_view,
    result_list,
    create_result,
    edit_result,
    delete_result,
    all_results
)

urlpatterns = [
    # Student public result
    path("student/result/", student_result_view, name="student_result"),

    # Admin result management
    path("admin/results/", all_results, name="result_list"),
    path("admin/results/create/", create_result, name="create_result"),
    path("admin/results/edit/<int:pk>/", edit_result, name="edit_result"),
    path("admin/results/delete/<int:pk>/", delete_result, name="delete_result"),
]
