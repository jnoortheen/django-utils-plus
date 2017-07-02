from django.http import HttpResponse


def return_path(request):
    return HttpResponse(request.path)
