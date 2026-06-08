from django.core.paginator import Paginator
from django.db.models import Q

def get_crud_context(request, queryset, headings, sort_allowed_fields, title, filter_fields=None, url_names=None):
    """
    Genera il contesto comune per le viste CRUD con filtraggio, ordinamento e paginazione.
    """
    # FILTRO
    filter_value = request.GET.get('filter', '')
    if filter_value and filter_fields:
        query = Q()
        for field in filter_fields:
            query |= Q(**{f"{field}__icontains": filter_value})
        queryset = queryset.filter(query)

    # ORDINAMENTO
    sort_field = request.GET.get('sort', 'id')
    sort_dir = request.GET.get('dir', '')
    if sort_field not in sort_allowed_fields:
        sort_field = 'id'

    # Preparazione headings per il template (next_dir)
    for h in headings:
        if h['key'] == sort_field:
            if sort_dir == 'asc': h['next_dir'] = 'desc'
            elif sort_dir == 'desc': h['next_dir'] = ''
            else: h['next_dir'] = 'asc'
        else:
            h['next_dir'] = 'asc'

    ordine = ""
    if sort_dir == 'desc':
        ordine = f"-{sort_field}"
    elif sort_dir == 'asc':
        ordine = sort_field
    
    if ordine:
        queryset = queryset.order_by(ordine)

    # PAGINAZIONE
    pagination_current_limit = request.GET.get('limit', '10')
    page_number = request.GET.get('page', 1)
    pagination_allowed_limits = ['5', '10', '20', '30', '50', '100']
    
    if pagination_current_limit not in pagination_allowed_limits:
        pagination_current_limit = '10'
    
    pagination_limit_int = int(pagination_current_limit)
    paginator = Paginator(queryset, pagination_limit_int)
    page_obj = paginator.get_page(page_number)

    return {
        'title': title,
        'object_list': page_obj,
        'headings': headings,
        'sort_field': sort_field,
        'sort_dir': sort_dir,
        'pagination_current_limit': pagination_current_limit,
        'pagination_allowed_limits': pagination_allowed_limits,
        'pagination_page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1),
        'filter_value': filter_value,
        'url_names': url_names or {},
    }
