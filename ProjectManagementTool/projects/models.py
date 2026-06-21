from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):

    project_name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.project_name

class Task(models.Model):

    STATUS_CHOICES = [

        ('todo', 'To Do'),

        ('progress', 'In Progress'),

        ('review', 'Review'),

        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [

        ('low', 'Low'),

        ('medium', 'Medium'),

        ('high', 'High'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    submitted_file = models.FileField(
    upload_to='task_submissions/',
    null=True,
    blank=True
    )
    submitted_at = models.DateTimeField(
    null=True,
    blank=True
    )
   
    is_submitted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.title


class Comment(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    comment_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

class ActivityLog(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=255
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.action

class Notification(models.Model):

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
        
class ProjectMember(models.Model):

    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

class TaskSubmission(models.Model):

    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    submitted_file = models.FileField(
        upload_to='task_submissions/'
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.task.title
    
