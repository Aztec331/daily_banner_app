from rest_framework.pagination import PageNumberPagination

class BannerPagination(PageNumberPagination):
    page_size = 10                  # default items per page
    page_size_query_param = 'limit' # frontend can override
    page_query_param = 'page'       # frontend sends ?page=1, ?page=2
    max_page_size = 100             # max items per page
