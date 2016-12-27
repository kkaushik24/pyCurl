from multiprocessing.pool import ThreadPool, TimeoutError

from django.shortcuts import render
from django.http import JsonResponse

from pcurl.utils import GoogleSearchService, DuckDuckGoSearchService
from pcurl.utils import TwitterSearchService


def psearch(request):
    """
    View to search multiple resource sites parallely for single request.
    It takes get parameter q and searches paralley in google, duckduckgo
    and twiter service.
    """
    # query to be searched for
    q = request.GET.get('q', '')

    # different type of search services
    search_services = [GoogleSearchService, DuckDuckGoSearchService,
                       TwitterSearchService]

    # initializing service objs here
    search_service_objs = [service(q) for service in search_services]

    # initializing pool for parallel processing
    pool = ThreadPool(processes=3)

    # dict comprehension for search dict in format
    # (key, value) = (service_obj, async service process)
    multiple_search_dict = {service_obj: pool.apply_async(service_obj.get_search_result)
                              for service_obj in search_service_objs}
    # response dict that holds the final result
    response_dict = {'query': q}

    # search result dict to hold the response from different service.
    search_results = {}
    for service_obj, search in multiple_search_dict.iteritems():
        search_result = ''
        error = ''
        service_dict = {}
        try:
            error, search_result = search.get(timeout=1)
        except TimeoutError:
            error = '{0} service timed out'.format(service_obj.service_type)
        service_dict = {
            'url': service_obj.get_rest_url(),
            'text': search_result,
            'error': error
        }
        search_results.update({service_obj.service_type: service_dict})
    response_dict.update({'results': search_results})
    return JsonResponse(response_dict)
