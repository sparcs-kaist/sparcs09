from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from sparcs09.apps.buy.models import Item, Option, Record, Payment


# /buy/
def main(request):
    items = Item.objects.filter(is_hidden=False).order_by('-id')
    if request.user.is_authenticated():
        for item in items:
            payment = Payment.objects.filter(item=item, user=request.user)
            item.payment = payment

    return render(request, 'main.html', {
                    'items': items,
                    'date': timezone.now(),
                 })


# /buy/list/
def record(request):
    items = Item.objects.all().order_by('-id')
    paginator = Paginator(items, 10)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        items = paginator.page(1)
        page = 1
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    start = page - 5
    end = page + 5
    if start < 1:
        start = 1
    if end > paginator.num_pages:
        end = paginator.num_pages

    if request.user.is_authenticated:
        for item in items:
            payment = Payment.objects.filter(item=item, user=request.user)
            item.payment = payment

    return render(request, 'list.html', {
                    'items': items,
                    'date': timezone.now(),
                    'cur_page': page,
                    'page_range': range(start, end + 1),
                    'has_previous': page > 1,
                    'has_next': page < paginator.num_pages,
                 })


# /buy/item/<pid>/
def item(request, pid):
    item = get_object_or_404(Item, id=pid)

    if request.method == 'POST':
        result = request.POST.get('data', '{}')
        return redirect('/buy/item/' + pid)

    records = []
    if request.user.is_authenticated():
        raw = Record.objects.filter(user=request.user)
        for r in raw:
            if r.option.item.id == int(pid):
                records.append(r)

    return render(request, 'item.html', {'item': item, 'date': timezone.now(), 'records': records})



# /buy/item/<pid>/list/
def item_total(request, pid):
    pass
