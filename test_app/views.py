from django.http import HttpRequest, HttpResponse


def greetings(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, user!")


