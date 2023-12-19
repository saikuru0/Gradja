from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def not_logged_in_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def has_required_group(user, allowed_groups):
    return user.groups.filter(name__in=allowed_groups).exists()



def user_with_required_group(*allowed_groups):
    def decorator(view_func):
        decorated_view_func = user_passes_test(lambda user: has_required_group(user, allowed_groups), login_url='home')(view_func)
        return decorated_view_func
    return decorator

