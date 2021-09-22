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


# def item_select(request, item_id):
#     item = get_object_or_404(Item, id=item_id)
#     if request.method == "POST":
#         form = SelectForm(item, request.POST)
#         if form.is_valid():
#             return redirect("profile")
#     else:
#         form = SelectForm(item)
#     return render(
#         request,
#         "baemin/select_form.html",
#         {
#             "form": form,
#             "item": item,
#         },
#     )


class ItemCreateView(CreateView):
    model = ItemProperty
    form_class = SelectForm
    template_name = "baemin/select_form.html"

    # https://dashdrum.com/blog/2018/02/passing-a-parameter-to-a-django-form/ 확인 필요 이 글을 통해서 값을 넘길 수 있었음

    def get_form(self, form_class=None):
        # item = get_object_or_404(Item, pk=self.kwargs["item_id"])
        # https://stackoverflow.com/questions/17906936/indexerror-tuple-index-out-of-range
        # https://yonghyunlee.gitlab.io/python/django-master-10/
        print(self)
        # self.kwargs {'item_id': 2}
        item = get_object_or_404(Item, pk=self.kwargs.get("item_id"))
        # item = get_object_or_404(Item, pk=self.args[1])
        if form_class is None:
            form_class = self.get_form_class()
        else:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), item=item)

    # def get_form(self, request, obj=None, **kwargs):
    #     kwargs["form"] = SelectForm
    #     return super().get_form(request, obj, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     print(super().get_form_kwargs())

    #     item = Item.objects.get(pk=1)
    #     self.object.item = item
    #     return super().form_valid(form)

    # def form_valid(self, form: _ModelFormT) -> HttpResponse:
    #     return super().form_valid(form)

    # def get_form_kwars(self):
    #     kwargs = super().get_form_kwargs()
    #     item = get_object_or_404(Item, pk=self.kwargs.get("pk"))
    #     kwargs["item"] = item
    #     return kwargs

    # def get_form_kwargs(self) -> Dict[str, Any]:
    #     return super().get_form_kwargs()

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     item = get_object_or_404(Item, pk=self.kwargs.get("pk"))
    #     context["item"] = "item"
    #     # OR
    #     # context.update({'item':item})
    #     return context

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     return super().get_context_data(**kwargs)

    # def get_object(self):
    #     item = get_object_or_404(Item, pk=self.kwargs["pk"])  # 4
    #     return item

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user

    # def form_valid(self, form: _ModelFormT) -> HttpResponse:
    #     return super().form_valid(form)

    # def get_object(self, queryset: Optional[models.query.QuerySet] = ...) -> T:
    #     return super().get_object(queryset=queryset)

    # def get_absolute_url(self):
    #     return reverse("baemin:item_detail", kwargs={"pk": self.pk})


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
