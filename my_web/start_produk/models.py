from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from .choices import STATUS_CHOICES, UNIT_CHOICES

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    identifier = models.CharField(max_length=50, unique=True, verbose_name="Идентификационный номер")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="Единица измерения")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма", blank=True, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="норма", verbose_name="Состояние")
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Distributor(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    region = models.CharField(max_length=100, verbose_name="Регион")
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    address_registration = models.CharField(max_length=255, verbose_name="Адрес по прописке")
    address_residence = models.CharField(max_length=255, verbose_name="Фактическое место жительства")
    passport_series = models.CharField(max_length=4, verbose_name="Серия паспорта")
    passport_number = models.CharField(max_length=6, verbose_name="Номер паспорта")
    passport_issued_by = models.CharField(max_length=255, verbose_name="Кем выдан")
    passport_issue_date = models.DateField(verbose_name="Дата выдачи")
    passport_expiry_date = models.DateField(verbose_name="Срок действия")
    phone_number_1 = models.CharField(max_length=15, verbose_name="Контактный номер 1")
    phone_number_2 = models.CharField(max_length=15, verbose_name="Контактный номер 2", null=True, blank=True)
    photo = models.ImageField(upload_to='distributors/', verbose_name="Фото", null=True, blank=True)
    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Дистрибьютор"
        verbose_name_plural = "Дистрибьюторы"

class SalesHistory(models.Model):
    distributor = models.ForeignKey(Distributor, related_name="sales_history", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    unique_code = models.CharField(max_length=100, verbose_name="Уникальный код", blank=True, null=True)
    unit = models.CharField(max_length=50, verbose_name="Единица измерения", blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    sale_date = models.DateField(verbose_name="Дата продажи")

    @property
    def total_sum(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"Продажа {self.product.name} - {self.quantity} шт."

    class Meta:
        verbose_name = "История продаж"
        verbose_name_plural = "Истории продаж"


class ReturnHistory(models.Model):
    distributor = models.ForeignKey(Distributor, related_name="return_history", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    unique_code = models.CharField(max_length=100, verbose_name="Уникальный код", blank=True, null=True)
    unit = models.CharField(max_length=50, verbose_name="Единица измерения", blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    return_date = models.DateField(verbose_name="Дата возврата")
    return_status = models.CharField(
        max_length=50,
        choices=[('normal', 'Норма'), ('defective', 'Брак')],
        verbose_name="Статус возврата"
    )

    @property
    def total_sum(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"Возврат {self.product.name} - {self.quantity} шт."

    class Meta:
        verbose_name = "История возврата"
        verbose_name_plural = "Истории возвратов"


class Order(models.Model):
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE, verbose_name="Дистрибьютор")
    invoice_number = models.CharField(max_length=100, unique=True, verbose_name="Номер накладной")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оформления")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Итоговая сумма")
    def __str__(self):
        return f"Заказ {self.invoice_number}"
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    @property
    def total(self):
        """Вычисляемая сумма позиции."""
        return self.quantity * self.price
    def save(self, *args, **kwargs):
        if self.quantity > self.product.quantity:
            raise ValidationError("Недостаточно товара на складе для выполнения заказа.")
        with transaction.atomic():
            super().save(*args, **kwargs)
            # Обновление количества на складе
            self.product.quantity -= self.quantity
            self.product.save()
    def __str__(self):
        return f"Товар {self.product.name} ({self.quantity} шт.)"
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"