from django.http import Http404, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.views import View
from .data import departures, tours


def custom_handler404(request, exception):
    return HttpResponseNotFound('Упс, не могу найти такую страницу...')


def custom_handler500(request, *args, **kwargs):
    return HttpResponseServerError('Упс, что то сломалось...')


class MainView(View):

    def get(self, request):
        return render(request, "tours/index.html")


class DepartureView(View):

    def get(self, request, departure: str):
        if departure in departures:
            return render(request, "tours/departure.html", departures)
        else:
            raise Http404


class TourView(View):

    def get(self, request, id: int):
        if id in tours:
            return render(request, "tours/tour.html", tours)
        else:
            raise Http404
