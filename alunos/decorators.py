from functools import wraps
from django.http import JsonResponse

def api_exception_handler(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return wrapper