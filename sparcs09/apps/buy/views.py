from django.shortcuts import render

# /buy/
def main(request):
    pass


# /buy/list/
def record(request):
    pass


# /buy/item/<pid>/
def item(request, pid):
    return render(request, 'item.html', {})


# /buy/item/<pid>/list/
def item_total(request, pid):
    pass
