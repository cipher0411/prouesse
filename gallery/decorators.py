from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

def student_member_required(view_func):
    def check_group(user):
        return user.groups.filter(name='student').exists()

    return user_passes_test(check_group)(view_func)

