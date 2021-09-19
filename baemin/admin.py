from django.contrib import admin
from .models import Shop, Item, Order, ItemProperty

# Register your models here.


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "tel", "addr")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "shop",
        "name",
    )
    list_filter = ("shop",)  # tuple 쓸꺼면 한개 넣을때는 뒤에 , 반드시 포함


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("shop", "user", "created_at")
    list_filter = (
        "shop",
        "user",
    )


@admin.register(ItemProperty)
class ItemDetailAdmin(admin.ModelAdmin):
    list_display = ("item", "price", "type")
    list_filter = ("item",)
