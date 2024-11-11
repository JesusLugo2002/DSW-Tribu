from django.http import HttpResponseForbidden, HttpResponse
from echos.models import Echo
from waves.models import Wave

def assert_owner_of(model: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = args[0].user
            match model.lower():
                case 'echo':
                    model_instance = Echo.objects.get(pk=kwargs['echo_pk'])
                case 'wave':
                    model_instance = Wave.objects.get(pk=kwargs['wave_pk'])
                case _:
                    return HttpResponse('ERROR: "assert_owner_of" decorator parameter not specified or specified wrongly! ("echo"|"wave").')
            if user != model_instance.user:
                return HttpResponseForbidden("Only the owner can do that!")
            return func(*args, **kwargs)
        return wrapper
    return decorator