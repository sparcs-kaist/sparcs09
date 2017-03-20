from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from apps.buy.models import Item, Option, Record, Payment


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

    if request.user.is_authenticated():
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

    if request.method == 'POST' and user.is_authenticated() and \
            item.valid_from < timezone.now() and timezone.now() < item.valid_to:
        raw_option = request.POST.getlist('option', [])
        raw_num = request.POST.getlist('num', [])
        if len(raw_option) != len(raw_num):
            return redirect('/buy/item/' + pid)

        data = {}; total = 0
        for i in range(len(raw_option)):
            option = Option.objects.filter(id=raw_option[i]).first()
            if not option or option.item != item:
                continue

            num = int(raw_num[i])
            if data.has_key(option.id):
                data[option.id] += num
            else:
                data[option.id] = num
            total += option.price * num

        records = Record.objects.filter(user=user, option__item__id=item.id)
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


    options = item.options.order_by('title')
    records = []; payment = None
    if user.is_authenticated():
        records = Record.objects.filter(user=user, option__item__id=item.id)
        payment = Payment.objects.filter(user=user, item=item).first()

    return render(request, 'item.html', {
                    'item': item,
                    'options': options,
                    'date': timezone.now(),
                    'records': records,
                    'payment': payment
                 })



# /buy/item/<pid>/list/
def item_total(request, pid):
    item = get_object_or_404(Item, id=pid)
    user = request.user

    payment = None
    payments = Payment.objects.filter(item=item)
    if user.is_authenticated():
        payment = Payment.objects.filter(user=user, item=item).first()

    options = Option.objects.filter(item=item).order_by('title')
    for option in options:
        records = Record.objects.filter(option=option)
        option.total_num = reduce(lambda num, rec: num + rec.num, records, 0)
        option.total_price = option.price * option.total_num

    return render(request, 'item-total.html', {
                    'item': item,
                    'date': timezone.now(),
                    'payment': payment,
                    'payments': payments,
                    'options': options,
                  })
