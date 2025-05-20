from functools import wraps
from django.http import JsonResponse

def log_event(event_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            
            # Preparar datos para LogRocket
            event_data = {
                'event': event_name,
                'user_id': request.user.id if request.user.is_authenticated else None,
                'path': request.path,
                'method': request.method,
            }
            
            # Si la respuesta es JSON, añadir los datos de LogRocket
            if isinstance(response, JsonResponse):
                response_data = response.content.decode('utf-8')
                if isinstance(response_data, dict):
                    response_data['logrocket_event'] = event_data
                    response = JsonResponse(response_data)
            
            return response
        return wrapped_view
    return decorator
