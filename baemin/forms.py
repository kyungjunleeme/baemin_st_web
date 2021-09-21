from django import forms
from django.forms import fields
from .models import ItemProperty, Order, Shop, Item


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("item_set",)

    def __init__(self, shop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields['item_set']) # <django.forms.models.ModelMultipleChoiceField object at 0x10c6a77c0>
        print(
            self.fields["item_set"].queryset
        )  # <django.forms.models.ModelMultipleChoiceField object at 0x10c6a77c0>
        self.fields["item_set"].queryset = self.fields["item_set"].queryset.filter(
            shop=shop
        )  # filter로 지정된 queryset만 넘겨라

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["item_set"].queryset = Item.objects.none()

    #     if "shop" in self.data:
    #         try:
    #             shop_id = int(self.data.get("shop"))
    #             self.fields["item_set"].queryset = Item.objects.filter(
    #                 shop=shop_id
    #             ).order_by("name")
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields["item_set"].queryset = self.instance.item_set.order_by("name")


class SelectForm(forms.ModelForm):
    class Meta:
        model = ItemProperty
        fields = ["item", "type"]

    def __init__(self, item, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields["item"].queryset)

        self.fields["item"].queryset = self.fields["item"].queryset.filter(
            id=item.id
        )  # filter로 지정된 queryset만 넘겨라
        choices = (("중", "중"), ("소", "소"))
        self.fields["type"] = forms.ChoiceField(choices=choices)  # label

        if "type" in self.data:
            print(self.data, "type")
            try:
                type_id = int(self.data.get("type"))
                self.fields["price"] = ItemProperty.objects.filter(type=type_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        # self.fields['item'].queryset = City.objects.none()

        # print(self.fields['item_set']) # <django.forms.models.ModelMultipleChoiceField object at 0x10c6a77c0>
