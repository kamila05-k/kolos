from rest_framework import generics, status
from rest_framework.response import Response
from .filters import ProductFilter
from .models import *
from .serializers import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        """
        Метод, который выполняет создание товара.
        Добавьте здесь дополнительную логику, если необходимо (например, логирование или настройку полей).
        """
        serializer.save()

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Используем pk для поиска товара по ID

    def perform_update(self, serializer):
        """
        Метод для выполнения обновления товара.
        """
        serializer.save()


# главный
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ProductFilter
    filterset_fields = ['status', 'category', 'unit']  # Фильтрация по статусу, категории и единице измерения
    ordering_fields = ['name', 'created_at']  # Сортировка по имени и дате создания
    ordering = ['name']  # Сортировка по имени по умолчанию

    def get_queryset(self):
        """
        Переопределение метода для добавления фильтрации по статусу, категории и единице измерения.
        """
        queryset = super().get_queryset()

        # Получаем параметры из запроса
        status = self.request.query_params.get('status', None)
        category = self.request.query_params.get('category', None)
        unit = self.request.query_params.get('unit', None)

        # Применяем фильтрацию по статусу
        if status:
            queryset = queryset.filter(status=status)

        # Применяем фильтрацию по категории
        if category:
            queryset = queryset.filter(category=category)

        # Применяем фильтрацию по единице измерения
        if unit:
            queryset = queryset.filter(unit=unit)

        return queryset
class ProductsUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'



class ArchiveProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_archived = True
        product.save()
        return Response({'message': 'Товар перемещен в архив'}, status=status.HTTP_200_OK)

# Восстановление товара из архива
class RestoreProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_archived = False
        product.save()
        return Response({'message': 'Товар восстановлен из архива'}, status=status.HTTP_200_OK)

# Отображение архива
class ArchivedProductsListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_archived=True)
    serializer_class = ProductSerializer


class DistributorListCreateView(generics.ListCreateAPIView):
    queryset = Distributor.objects.filter(is_archived=False)
    serializer_class = DistributorSerializer

    def perform_create(self, serializer):
        serializer.save()


class DistributorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer

    def perform_update(self, serializer):
        """
        Обновление данных дистрибьютора
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Архивирование дистрибьютора, а не удаление
        """
        instance.is_archived = True
        instance.save()


class DistributorArchiveView(generics.ListAPIView):
    queryset = Distributor.objects.filter(is_archived=True)
    serializer_class = DistributorSerializer


class SalesHistoryListCreateView(generics.ListCreateAPIView):
    """
    Представление для списка и создания истории продаж.
    """
    queryset = SalesHistory.objects.all()
    serializer_class = SalesHistorySerializer

    def perform_create(self, serializer):
        """
        Сохранение новой записи о продаже.
        """
        serializer.save()


class SalesHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления истории продаж.
    """
    queryset = SalesHistory.objects.all()
    serializer_class = SalesHistorySerializer


class ReturnHistoryListCreateView(generics.ListCreateAPIView):
    """
    Представление для списка и создания истории возврата.
    """
    queryset = ReturnHistory.objects.all()
    serializer_class = ReturnHistorySerializer

    def perform_create(self, serializer):
        """
        Сохранение новой записи о возврате.
        """
        serializer.save()


class ReturnHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления истории возврата.
    """
    queryset = ReturnHistory.objects.all()
    serializer_class = ReturnHistorySerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        """
        Создание нового заказа. Обработаем дополнительную логику.
        """
        serializer.save()

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Обновление данных заказа.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Логика удаления заказа (например, поместить его в архив или обновить статус).
        """
        instance.delete()

class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        """
        Создание новой позиции в заказе.
        """
        order_item = serializer.save()

        # Обновляем количество товара в заказе
        product = order_item.product
        if order_item.quantity > product.quantity:
            raise ValidationError("Недостаточно товара на складе для выполнения заказа.")

        # Обновление количества товара на складе
        product.quantity -= order_item.quantity
        product.save()

        return order_item

class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        """
        Обновление позиции заказа. Обработаем логику изменения количества товара.
        """
        order_item = serializer.save()

        # Проверяем, достаточно ли товара на складе
        if order_item.quantity > order_item.product.quantity:
            raise ValidationError("Недостаточно товара на складе для выполнения заказа.")

        # Обновление количества товара на складе
        order_item.product.quantity -= order_item.quantity
        order_item.product.save()

        return order_item

    def perform_destroy(self, instance):
        """
        Удаление позиции заказа и восстановление товара на складе.
        """
        product = instance.product
        product.quantity += instance.quantity
        product.save()
        instance.delete()

class OrderItemRestoreStockView(generics.UpdateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def update(self, request, *args, **kwargs):
        order_item = self.get_object()
        order_item.product.quantity += order_item.quantity
        order_item.product.save()
        return Response({'message': 'Товар восстановлен на складе'}, status=status.HTTP_200_OK)
