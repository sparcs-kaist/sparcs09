from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from sparcs09.apps.buy.models import Item, Option, Record, Payment


def get_records(user, pid):
    records = []
    raw = Record.objects.filter(user=user)
    for r in raw:
        if r.option.item.id == pid:
            records.append(r)
    return records


# /buy/
def main(request):
    items = Item.objects.filter(is_hidden=False).order_by('-id')
    if request.user.is_authenticated():
        for item in items:
            payment = Payment.objects.filter(item=item, user=request.user).first()
            item.payment = payment

    return render(request, 'main.html', {'items': items, 'date': timezone.now()})


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
            payment = Payment.objects.filter(item=item, user=request.user).first()
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
    user = request.user

    if request.method == 'POST' and user.is_authenticated():
        raw_option = request.POST.getlist('option', [])
        raw_num = request.POST.getlist('num', [])
        if len(raw_option) != len(raw_num):
            return HttpResponseBadRequest()

        data = {}; total = 0
        for i in range(len(raw_option)):
            option = get_object_or_404(Option, id=raw_option[i])
            if option.item != item:
                continue

            num = int(raw_num[i])
            if data.has_key(option.id):
                data[option.id] += num
            else:
                data[option.id] = num
            total += option.price * num

        records = get_records(user, item.id)
        for record in records:
            record.delete()

        for k, v in data.iteritems():
            option = Option.objects.get(id=k)
            Record(user=user, option=option, num=v).save()

        payments = Payment.objects.filter(user=user, item=item)
        for payment in payments:
            payment.delete()

        if total > 0:
            Payment(user=user, item=item, total=total, is_paid=False).save()

        return redirect('/buy/item/' + pid)


    records = []; payment = None
    if user.is_authenticated():
        records = get_records(user, item.id)
        payment = Payment.objects.filter(user=user, item=item).first()

    return render(request, 'item.html', {
                    'item': item,
                    'date': timezone.now(),
                    'records': records,
                    'payment': payment
                 })



# /buy/item/<pid>/list/
def item_total(request, pid):
    pass
