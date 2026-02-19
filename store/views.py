from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .models import Cart, CartItem, Category, Product


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None

    cart, _ = Cart.objects.get_or_create(session_key=session_key, defaults={"user": user})

    if user and cart.user_id is None:
        cart.user = user
        cart.save(update_fields=["user"])

    return cart


class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        category_id = self.request.GET.get("category")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        context["cart"] = get_or_create_cart(self.request)
        return context


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, quantity)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=["quantity"])

    messages.success(request, f"Added {quantity} x {product.name} to cart.")

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)

    return redirect("product_list")


def cart_detail(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product")

    return render(
        request,
        "store/cart.html",
        {
            "cart": cart,
            "items": items,
        },
    )
