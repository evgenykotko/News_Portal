from django.shortcuts import render
from django.utils.translation import gettext as _  # импортируем функцию для перевода
from django.views import View
from django.http import HttpResponse

class Test(View):
    def get(self, request):
        string = _('Hello world')
        context = {
            'string': string
        }

        return HttpResponse(render(request, 'test.html', context))