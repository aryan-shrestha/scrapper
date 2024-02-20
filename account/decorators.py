from functools import wraps
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def user_in_groups(groups):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            super_admin = Group.objects.get(name='super admin')
            
            # check if user is in super admin groum
            if super_admin in user.groups.all():
                return view_func(request, *args, **kwargs)

            # Check if the user is in any of the specified groups
            if any(group in groups for group in user.groups.values_list('name', flat=True)):
                return view_func(request, *args, **kwargs)

            # Redirect or handle unauthorized access
            messages.error(request, "Unauthorized")
            logout(request)
            return redirect('account:login_view')

        return _wrapped_view

    return decorator