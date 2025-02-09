from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def gym_owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'gymowner'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view

def trainer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'trainer'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view

def gym_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'gymuser'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view
