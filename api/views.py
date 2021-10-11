from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from datetime import datetime
from django.core.cache import cache


# Create your views here.
def index(request):
    return JsonResponse({"status": 200})


class RawDataView(APIView):

    def get(self, request, format=None):
        if 'pageSize' not in request.GET:
            return JsonResponse({"status": 400, 'detail':'The page size parameter is not set'})

        # get data if exists in cache entries area
        entries = cache.get('entries')

        # set the page size value
        pageSize = int(request.GET.get("pageSize"))

        # set the update mode value
        updateMode = int(request.GET.get("updateMode", False))

        '''
            Check the entries status
            If the entries status is empty generate 50000 entries
            Else get the page size emtries results and send them to consumedata command
            to be processed and added to db
        '''
        if not entries:
            entries = cache.set("entries", generate_entries(50000, updateMode))
            return Response({"results":[], "pageSize": pageSize, "remaining": 50000})
        else:
            # set the page size result
            result = entries[:pageSize]

            '''
                check if the result number it is < then page size and clear the redis cache
                or update the redis cache entries with remaining entries
            '''
            if len(result) < pageSize:
                cache.delete('entries')
            else:
                cache.set('entries', entries[pageSize:])

            # return the results, page size and  the remaining entries number
            return Response({"results": result, "pageSize": pageSize, "remaining": len(entries) - len(result)})


def generate_entries(count, updateMode=False):
    # get or set the last entry flag
    lastEntry = cache.get_or_set("lastEntry", 0) if not updateMode else 0

    # set the result list holder
    result = []

    # create the list
    for i in range(count):
        rawData = {
            "network_app": f"network_app {lastEntry + i}",
            "network_campaign": f"network_campaign {lastEntry + i} {'updated' if updateMode else ''}",
            "network_adgroup": f"network_adgroup {lastEntry + i} {'updated' if updateMode else ''}",
            "taps": lastEntry + i,
            "views": lastEntry + i,
            "cost": float(i),
            "earnings": float(i),
        }

        # add the created dict to list holder
        result.append(rawData)

    # return the list holder
    return result
