from django.shortcuts import render
from .models import Products, Order
from django.core.paginator import Paginator
import json

def index(request):
    product_objects = Products.objects.all()

    # Search code
    item_name = request.GET.get('item_name')
    if item_name:
        product_objects = product_objects.filter(title__icontains=item_name)

    # Paginator code
    paginator = Paginator(product_objects, 2)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    return render(request, 'shop/index.html', {'product_objects': product_objects})


def detail(request, id):
    product_object = Products.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('items', '{}')

        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            items = {}

        if not items or items == {}:
            return render(request, 'shop/checkout.html', {'success': False, 'empty': True})

        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zipcode = request.POST.get("zipcode", "")

        total = 0
        for item in items.values():
            if len(item) == 3:
                qty, _, price = item
                total += qty * price

        # Save order
        order = Order(
            items=items_json,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            total=total
        )
        order.save()

        return render(request, 'shop/checkout.html', {
            'success': True,
            'total': total
        })

    return render(request, 'shop/checkout.html')