from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=100)  # 이름
    tel = models.CharField(max_length=20)  # RegexValidator 추가 가능 # 전화번호
    addr = models.CharField(max_length=100)  # 주소

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("baemin:shop_detail", kwargs={"pk": self.pk})


class Item(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 가게
    name = models.CharField(max_length=100)  # 이름

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("baemin:item_detail", kwargs={"pk": self.pk})


class ItemProperty(models.Model):

    # class Suit(models.IntegerChoices):
    #     DIAMOND = 1 # 이렇게 모델 생성 시 바로 생성되면 안되고, 사용자가 바꿀수 있어야 하는데.....못바꾸기 때문에 사용 못함
    #     SPADE = 2
    #     HEART = 3
    #     CLUB = 4

    # suit = models.IntegerField(choices=Suit.choices)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, null=True, blank=True)  # 타입이 없을 수도 있음
    price = models.PositiveIntegerField()  # 가격

    # 각종 메뉴 안에서도 대/중/소 말고 다른 옵션들 어떻게 넣는지 생각

    def __str__(self):
        return str(self.price)


class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 가게
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # 주문한 유저
    item_set = models.ManyToManyField(Item)  # 주문한 상품 목록 (Hint: ManyToManyField)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일시

    class Meta:
        ordering = ("-id",)

    def get_absolute_url(self):
        return reverse("baemin:order_detail", kwargs={"pk": self.pk})

    # @property
    # def total(self):
    #     return sum(item.price for item in self.item_set.all())

    # Author.objects.annotate(total_pages=Sum('book__pages'))
