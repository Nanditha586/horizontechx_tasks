from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .utils import send_notification
from .forms import ProjectForm, TaskForm
from .models import Project
from .models import Project, Task, Notification, ProjectMember, ActivityLog, Comment
from .permissions import is_owner, is_manager, is_member

@login_required
def create_project(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(
                commit=False
            )

            project.created_by = request.user

            project.save()
            ProjectMember.objects.create(

    project=project,

    user=request.user,

    role='owner'

)

            return redirect(
                'project_list'
            )

    else:

        form = ProjectForm()

    return render(
        request,
        'projects/create_project.html',
        {'form': form}
    )
@login_required
def project_list(request):

    projects = Project.objects.filter(
        created_by=request.user
    )

    return render(
        request,
        'projects/project_list.html',
        {'projects': projects}
    )


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Project,
    Task,
    ProjectMember,
    ActivityLog,
    Notification
)

from .forms import TaskForm

from .permissions import (
    is_owner,
    is_manager
)


@login_required
def create_task(request, project_id):
    

    project = get_object_or_404(
        Project,
        id=project_id
    )
    print("User:", request.user)
    print("Project:", project.project_name)

    print("Owner Check:", is_owner(request.user, project))
    print("Manager Check:", is_manager(request.user, project))

    #if not (
     #   is_owner(request.user, project)
       # or
       # is_manager(request.user, project)
    #):
       # return redirect('board_view', project.id)

    if request.method == "POST":

        form = TaskForm(request.POST)

    else:

        form = TaskForm()

    # Show only project members
    member_ids = ProjectMember.objects.filter(
        project=project
    ).values_list(
        'user_id',
        flat=True
    )

    form.fields['assigned_to'].queryset = User.objects.filter(
        id__in=member_ids
    )

    if request.method == "POST" and form.is_valid():

        task = form.save(commit=False)

        task.project = project

        task.save()

        ActivityLog.objects.create(
            project=project,
            user=request.user,
            action=f"Created task '{task.title}'"
        )

        if task.assigned_to:

            Notification.objects.create(
                receiver=task.assigned_to,
                message=f"You have been assigned task '{task.title}'"
            )

        return redirect(
            'board_view',
            project.id
        )

    return render(
        request,
        'projects/create_task.html',
        {
            'form': form,
            'project': project
        }
    )

@login_required
def board_view(request, project_id):

    project = Project.objects.get(
        id=project_id
    )

    todo_tasks = Task.objects.filter(
        project=project,
        status='todo'
    )

    progress_tasks = Task.objects.filter(
        project=project,
        status='progress'
    )

    review_tasks = Task.objects.filter(
        project=project,
        status='review'
    )

    done_tasks = Task.objects.filter(
        project=project,
        status='done'
    )

    context = {

        'project': project,

        'todo_tasks': todo_tasks,

        'progress_tasks': progress_tasks,

        'review_tasks': review_tasks,

        'done_tasks': done_tasks,
    }

    return render(
        request,
        'projects/board.html',
        context
    )
from django.contrib import messages
from django.contrib.auth.models import User

from .models import (
    Project,
    ProjectMember,
    ActivityLog,
    Notification
)

from .permissions import is_owner

@login_required
def add_member(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        email = request.POST.get('email')

        try:

            user = User.objects.get(
                email=email
            )

            if ProjectMember.objects.filter(
                project=project,
                user=user
            ).exists():

                messages.error(
                    request,
                    "User is already a member of this project."
                )

            else:

                ProjectMember.objects.create(
                    project=project,
                    user=user,
                    role='member'
                )

                messages.success(
                    request,
                    f"{user.username} added successfully."
                )

                return redirect(
                    'project_members',
                    project.id
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "No registered user found with this email."
            )

    return render(
        request,
        'projects/add_member.html',
        {
            'project': project
        }
    )
@login_required
def add_comment(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == "POST":

        text = request.POST.get(
            'comment_text'
        )

        comment = Comment.objects.create(
            task=task,
            user=request.user,
            comment_text=text
        )

        # Notify assigned member

        if (
            task.assigned_to
            and
            task.assigned_to != request.user
        ):

            Notification.objects.create(
                receiver=task.assigned_to,
                message=
                f"{request.user.username} commented on task '{task.title}'"
            )

        return redirect(
            'task_detail',
            task.id
        )    
from django.core.paginator import Paginator

@login_required
def notifications(request):

    notification_list = Notification.objects.filter(
        receiver=request.user
    ).order_by('-created_at')  # Latest first

    paginator = Paginator(
        notification_list,
        10
    )

    page_number = request.GET.get('page')

    notifications = paginator.get_page(
        page_number
    )
    Notification.objects.filter(
        receiver=request.user,
        is_read=False
        ).update(is_read=True)
    return render(
        request,
        'projects/notifications.html',
        {
            'notifications': notifications
        }
    )

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectMember

@login_required
def change_role(request, project_id, member_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    member = get_object_or_404(
        ProjectMember,
        id=member_id,
        project=project
    )

    if request.method == "POST":

        role = request.POST.get("role")

        member.role = role
        member.save()
    print("Selected Role:", request.POST.get("role"))
    return redirect(
        "project_members",
        project_id=project.id
    )

@login_required
def project_members(
    request,
    project_id
):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    members = ProjectMember.objects.filter(
        project=project
    ).select_related(
        'user'
    )

    return render(
        request,
        'projects/members.html',
        {
            'project': project,
            'members': members
        }
    )

@login_required
def delete_project(
    request,
    project_id
):

    project = Project.objects.get(
        id=project_id
    )

    if is_owner(
        request.user,
        project
    ):

        project.delete()

    return redirect(
        'project_list'
    )


@login_required
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            ActivityLog.objects.create(
                project=task.project,
                user=request.user,
                action=f"Updated task '{task.title}'"
            )

            return redirect(
                'board_view',
                task.project.id
            )

    else:

        form = TaskForm(
            instance=task
        )

    return render(
        request,
        'projects/edit_task.html',
        {
            'form': form,
            'task': task
        }
    )
@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    project_id = task.project.id

    ActivityLog.objects.create(
        project=task.project,
        user=request.user,
        action=f"Deleted task '{task.title}'"
    )

    task.delete()

    return redirect(
        'board_view',
        project_id
    )
@login_required
def update_task_status(
    request,
    task_id,
    status
):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    task.status = status

    task.save()

    ActivityLog.objects.create(
        project=task.project,
        user=request.user,
        action=f"Moved task '{task.title}' to {status}"
    )

    return redirect(
        'board_view',
        task.project.id
    )

@login_required
def task_detail(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    comments = Comment.objects.filter(
        task=task
    ).order_by(
        'created_at'
    )

    return render(
        request,
        'projects/task_detail.html',
        {
            'task': task,
            'comments': comments
        }
    )

@login_required
def activity_logs(
    request,
    project_id
):

    project = Project.objects.get(
        id=project_id
    )

    logs = ActivityLog.objects.filter(
        project=project
    ).order_by(
        '-timestamp'
    )

    return render(
        request,
        'projects/activity_logs.html',
        {
            'logs': logs,
            'project': project
        }
    )

from django.db.models import Count
from .models import (
    Project,
    Task,
    ProjectMember,
    ActivityLog
)

@login_required
def analytics_dashboard(request):

    # Projects where current user is a member
    project_count = ProjectMember.objects.filter(
        user=request.user
    ).count()

    # Tasks assigned to current user
    assigned_tasks = Task.objects.filter( assigned_to=request.user)
    
    assigned_count = assigned_tasks.count()

    completed_tasks = assigned_tasks.filter(
        status='done'
    ).count()

    pending_tasks = assigned_tasks.exclude(
        status='done'
    ).count()

    total_members = ProjectMember.objects.count()

    if assigned_count > 0:

        completion_percentage = round(
            (completed_tasks / assigned_count) * 100,
            2
        )

    else:

        completion_percentage = 0

    high_priority = assigned_tasks.filter(
        priority='high'
    ).count()

    medium_priority = assigned_tasks.filter(
        priority='medium'
    ).count()

    low_priority = assigned_tasks.filter(
        priority='low'
    ).count()

    recent_logs = ActivityLog.objects.order_by(
        '-timestamp'
    )[:10]

    unread_notifications = Notification.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    context = {

        'project_count': project_count,

        'assigned_count': assigned_count,
        'assigned_tasks': assigned_tasks,
        'completed_tasks': completed_tasks,

        'pending_tasks': pending_tasks,

        'total_members': total_members,

        'completion_percentage': completion_percentage,

        'high_priority': high_priority,

        'medium_priority': medium_priority,

        'low_priority': low_priority,

        'recent_logs': recent_logs,

        'unread_notifications': unread_notifications,
    }

    return render(
        request,
        'projects/analytics_dashboard.html',
        context
    )

from django.utils import timezone

@login_required
def submit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if request.user != task.assigned_to:

        return redirect('dashboard')

    if request.method == "POST":

        task.submitted_file = request.FILES.get(
            'submitted_file'
        )

        task.is_submitted = True

        task.submitted_at = timezone.now()

        task.save()

        Notification.objects.create(
            receiver=task.project.created_by,
            message=f"{request.user.username} submitted task '{task.title}'"
        )

        return redirect('dashboard')

    return render(
        request,
        'projects/submit_task.html',
        {
            'task': task
        }
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
@login_required
def submitted_tasks(request):

    tasks = Task.objects.filter(
        is_submitted=True
    )

    owner_projects = ProjectMember.objects.filter(
        user=request.user,
        role__in=['owner','manager']
    ).values_list(
        'project_id',
        flat=True
    )

    tasks = tasks.filter(
        project_id__in=owner_projects
    )

    return render(
        request,
        'projects/submitted_tasks.html',
        {
            'tasks': tasks
        }
    )
from django.http import FileResponse

@login_required
def download_submission(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id
    )

    if not task.submitted_file:
        return redirect('submitted_tasks')

    return FileResponse(
        task.submitted_file.open('rb'),
        as_attachment=True,
        filename=task.submitted_file.name.split('/')[-1]
    )

@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if comment.user != request.user:
        return redirect(
            'task_detail',
            comment.task.id
        )

    if request.method == "POST":

        comment.comment_text = request.POST.get(
            'comment_text'
        )

        comment.save()

        return redirect(
            'task_detail',
            comment.task.id
        )

    return render(
        request,
        'projects/edit_comment.html',
        {'comment': comment}
    )


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if comment.user != request.user:
        return redirect(
            'task_detail',
            comment.task.id
        )

    task_id = comment.task.id

    if request.method == "POST":

        comment.delete()

        return redirect(
            'task_detail',
            task_id
        )

    return render(
        request,
        'projects/delete_comment.html',
        {'comment': comment}
    )

from .models import TaskSubmission, Comment


@login_required
def submission_detail(request, submission_id):

    submission = get_object_or_404(
        TaskSubmission,
        id=submission_id
    )

    task = submission.task

    comments = Comment.objects.filter(
        task=task
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'projects/submission_detail.html',
        {
            'submission': submission,
            'task': task,
            'comments': comments
        }
    )
from django.utils import timezone

@login_required
def member_submission_details(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        assigned_to=request.user
    )

    comments = Comment.objects.filter(
        task=task
    ).order_by('-created_at')

    if request.method == "POST":

        if request.FILES.get('submitted_file'):

            task.submitted_file = request.FILES[
                'submitted_file'
            ]

            task.is_submitted = True

            task.submitted_at = timezone.now()

            task.save()

            Notification.objects.create(
                receiver=task.project.created_by,
                message=f"{request.user.username} re-uploaded file for task '{task.title}'"
            )

    return render(
        request,
        'projects/member_submission_detail.html',
        {
            'task': task,
            'comments': comments
        }
    )