from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )

    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def count_price(self):
        total_price = self.annotate(amount=Sum(
            F('orders__quantity') * F('orders__product_price')))
        return total_price


class Order(models.Model):

    UNPROCESSED = 'unprocessed'
    RECIVE = 'RE'
    PREPARING = 'PR'
    DELIVERY = 'DE'
    DONE = 'DO'
    STATUS = [
        (UNPROCESSED, 'Необработано'),
        (RECIVE, 'Получено'),
        (PREPARING, 'Подготовка'),
        (DELIVERY, 'Доставка'),
        (DONE, 'Выполнено'),
    ]
    CASH = 'CASH'
    CARD = 'CARD'

    PAYMENT = [
        (CASH, 'Наличные'),
        (CARD, 'Безнал')

    ]

    registered_at = models.DateTimeField(
        'Зарегистрировано', default=timezone.now, null=True)
    called_at = models.DateTimeField('Подтверждено', null=True, blank=True)
    delivered_at = models.DateTimeField('Доставлено', null=True, blank=True)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='restaurants',
        verbose_name='Ресторан',
        null=True,
        blank=True
    )
    payment = models.CharField('Cпособ оплаты', max_length=20, choices=PAYMENT)
    status = models.CharField('Статус', max_length=20,
                              default=UNPROCESSED, choices=STATUS)
    firstname = models.CharField('Имя', max_length=50)
    lastname = models.CharField('Фамилия', max_length=50, blank=True)
    phonenumber = PhoneNumberField('Телефон', region="RU")
    address = models.CharField('Адрес', max_length=250)
    comment = models.TextField('Комментарий', blank=True)
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname} , {self.address}"


class OrderDetails(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='selected_products',
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[MinValueValidator(1)]
    )
    product_price = models.DecimalField(
        verbose_name='цена товара',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self) -> str:
        return f"{self.order}"


