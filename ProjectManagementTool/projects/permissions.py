from .models import ProjectMember


def is_owner(user, project):

    return ProjectMember.objects.filter(

        user=user,

        project=project,

        role='owner'

    ).exists()


def is_manager(user, project):

    return ProjectMember.objects.filter(

        user=user,

        project=project,

        role='manager'

    ).exists()


def is_member(user, project):

    return ProjectMember.objects.filter(

        user=user,

        project=project

    ).exists()