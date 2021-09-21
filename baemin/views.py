from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import ItemProperty, Shop, Order, Item
from .forms import OrderForm, SelectForm


# Create your views here.
# def index(request):
#     return render(request, "baemin/index.html")


class ShopListView(ListView):
    model = Shop
    template_name = "baemin/index.html"


class ShopDetailView(DetailView):
    model = Shop

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context["item_set"] = self.object.item_set.all()
        context["item_property"] = self.object.item_set.first().itemproperty_set.all()
        # print(context)
        return self.render_to_response(context)


class ItemDetailView(DetailView):
    model = Item

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        print(context)  #
        return self.render_to_response(context)


@login_required
def order_new(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    if request.method == "POST":
        form = OrderForm(shop, request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.shop = shop
            order.save()
            # 필히 호출. form.save 내에서 save_m2m()이 호출되는데, commit=False시에는 호출되지 않음. 그러므로 order.save() 와 form.save_m2m()은 한 set
            form.save_m2m()
            return redirect("profile")
    else:
        form = OrderForm(shop)
    return render(
        request,
        "baemin/order_form.html",
        {
            "form": form,
            "shop": shop,
        },
    )


class OrerDetailView(DetailView):
    model = Order


# class OrderCreateView(CreateView):
#     model = Order
#     form_class = OrderForm

#     # def get_object(self, queryset: Optional[models.query.QuerySet] = ...) -> T:
#     #     return super().get_object(queryset=queryset)

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.shop = self.get_object()
#         self.object.save()
#         form.save_m2m()
#         return super().form_valid(form)


def item_select(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        form = SelectForm(item, request.POST)
        if form.is_valid():
            return redirect("profile")
    else:
        form = SelectForm(item)
    return render(
        request,
        "baemin/select_form.html",
        {
            "form": form,
            "item": item,
        },
    )


class ItemPropertyListView(ListView):
    model = ItemProperty
    # context_object_name = "재정의하고 싶은 이름"


class ItemPropertyCreateView(CreateView):
    model = ItemProperty
    form_class = SelectForm
    success_url = reverse_lazy("itempropery_changelist")


class ItemPropertyUpdateView(UpdateView):
    model = ItemProperty
    form_class = SelectForm
    success_url = reverse_lazy("itempropery_changelist")


def load_prices(request):
    type_id = request.GET.get("type")
    print(type_id)
    prices = ItemProperty.objects.filter(type=type_id)
    print(prices)
    return render(
        request, "baemin/prices_dropdown_list_options.html", {"prices": prices}
    )
