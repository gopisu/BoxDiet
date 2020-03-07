from django.core.paginator import Paginator


def count(model):
    return model.objects.all().count()


def sliced_paginator(request, object_list):
    paginator = Paginator(object_list, 30)
    page = request.GET.get("page")
    object_list = paginator.get_page(page)
    index = object_list.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    return page_range, object_list


def validate_int(variable):
    try:
        var2 = int(variable)
    except ValueError:
        return False
    return var2
