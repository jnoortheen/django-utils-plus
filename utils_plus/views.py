from django.http import HttpResponse


def return_path(request, *args, **kwargs):
    return HttpResponse("Requested " + request.path + "with Args: {} {}".format(args, kwargs))
