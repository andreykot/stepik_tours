from random import sample
from django.http import Http404, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from .data import title, subtitle, description, departures, tours


def custom_handler404(request, exception):
    return HttpResponseNotFound('Упс, не могу найти такую страницу...')


def custom_handler500(request, *args, **kwargs):
    return HttpResponseServerError('Упс, что то сломалось...')


class MainView(View):

    def get(self, request):
        unique_tours = sample(list(tours.keys()), 6)

        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'tours': {i: tours[i] for i in unique_tours},
            'departures': departures
        }
        return render(request, "tours/index.html", context)


class DepartureView(View):

    def get(self, request, departure: str):
        if departure in departures:
            city_tours = {}
            min_price, max_price = float('inf'), float('-inf')
            min_nights, max_nights = float('inf'), float('-inf')
            for idx, tour in tours.items():
                if tour['departure'] == departure:
                    city_tours[idx] = tour
                    min_price = tour['price'] if min_price > tour['price'] else min_price
                    max_price = tour['price'] if max_price < tour['price'] else max_price
                    min_nights = tour['nights'] if min_nights > tour['nights'] else min_nights
                    max_nights = tour['nights'] if max_nights < tour['nights'] else max_nights

            context = {
                'departure_code': departure,
                'departure_city': departures[departure].split(' ')[1],
                'departures': departures,
                'tours': city_tours,
                'tours_number': len(city_tours),
                'min_price': min_price,
                'max_price': max_price,
                'min_nights': min_nights,
                'max_nights': max_nights,
            }

            return render(request, "tours/departure.html", context)
        else:
            raise Http404


class TourView(View):

    def get(self, request, id: int):
        if id in tours:
            context = {
                'info': tours[id],
                'departure_text': departures[tours[id]['departure']],
                'departure_code': tours[id]['departure'],
                'departures': departures,
            }

            return render(request, "tours/tour.html", context)
        else:
            raise Http404
