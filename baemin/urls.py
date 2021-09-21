from django.urls import path
from . import views

app_name = "baemin"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.ShopListView.as_view(), name="index"),
    path("orders/<int:pk>/", views.OrerDetailView.as_view(), name="order_detail"),
    path("shops/<int:pk>/", views.ShopDetailView.as_view(), name="shop_detail"),
    path("items/<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("<int:item_id>/new/", views.item_select, name="item_select"),
    path(
        "ajax/load_prices/", views.load_prices, name="load_prices"
    ),  # <-- this one here
    # path("orders/", views.OrderListView.as_view(), name="order_changelist"),
    # path("orders/add/", views.OrderCreateView.as_view(), name="order_add"),
    # path("orders/<int:pk>/", views.OrderUpdateView.as_view(), name="order_change"),
]

# baemin/shops/11/
# baemin/orders/11/
# Generic detail view ShopDetailView must be called with either an object pk or a slug in the URLconf.
# https://www.valentinog.com/blog/detail/ "uuid 추가하는 법"
# path("<int:shop_id>/new/", views.order_new, name="order_new"),
