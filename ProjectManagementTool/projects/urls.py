from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/',
        views.create_project,
        name='create_project'
    ),

    path(
        '',
        views.project_list,
        name='project_list'
    ),
    path(
    '<int:project_id>/board/',
    views.board_view,
    name='board_view'
),
path(
    'task/<int:task_id>/submit/',
    views.submit_task,
    name='submit_task'
),
path(
    'submitted-tasks/',
    views.submitted_tasks,
    name='submitted_tasks'
),

path(
    '<int:project_id>/task/create/',
    views.create_task,
    name='create_task'
),
path(
    '<int:project_id>/member/add/',
    views.add_member,
    name='add_member'
),

path(
    'task/<int:task_id>/comment/',
    views.add_comment,
    name='add_comment'
),

path(
    'notifications/',
    views.notifications,
    name='notifications'
),
path('<int:project_id>/activity/', views.activity_logs, name='activity_logs'),
path(

    '<int:project_id>/members/',

    views.project_members,

    name='project_members'

),

path(
    '<int:project_id>/members/<int:member_id>/change-role/',
    views.change_role,
    name='change_role'
),
path(
    'task/<int:task_id>/edit/',
    views.edit_task,
    name='edit_task'
),

path(
    'task/<int:task_id>/delete/',
    views.delete_task,
    name='delete_task'
),

path(
    'task/<int:task_id>/status/<str:status>/',
    views.update_task_status,
    name='update_task_status'
),
path(
    'task/<int:task_id>/',
    views.task_detail,
    name='task_detail'
),
path(
    'analytics/',
    views.analytics_dashboard,
    name='analytics_dashboard'
),
path(
    'comment/<int:comment_id>/edit/',
    views.edit_comment,
    name='edit_comment'
),
path(
    'comment/<int:comment_id>/delete/',
    views.delete_comment,
    name='delete_comment'
),
path(
    'download/<int:task_id>/',
    views.download_submission,
    name='download_submission'
),
path(
    'submission/<int:submission_id>/',
    views.submission_detail,
    name='submission_detail'
),
path(
    'member/submission/<int:task_id>/',
    views.member_submission_details,
    name='member_submission_details'
),
]