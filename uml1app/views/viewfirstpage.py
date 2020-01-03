from django.http import HttpResponse
from django.template import loader


def firstpage(request):
    template = loader.get_template("uml1app/firstpage.html")
    return HttpResponse(template.render())
