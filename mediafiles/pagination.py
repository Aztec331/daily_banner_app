# mediafiles/pagination.py
from rest_framework.pagination import PageNumberPagination

class MediaPagination(PageNumberPagination):
    page_size = 10  # default items per page
    page_size_query_param = "limit"  # use ?limit=
    page_query_param = "page"  # use ?page=
    max_page_size = 100
