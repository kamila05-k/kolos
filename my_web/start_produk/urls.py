from django.urls import path
from .views import *
urlpatterns = [
    path('product/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('product/update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product-update'),
    # главный
    path('home/list', ProductListAPIView.as_view(), name='product-list'),
    path('home/update/<int:pk>/list', ProductsUpdateAPIView.as_view(), name='product-update-delete'),
# архив
    path('product/archive/<int:pk>/', ArchiveProductView.as_view(), name='archive-product'),
    path('product/restore/<int:pk>/', RestoreProductView.as_view(), name='restore-product'),
    path('product/archived/', ArchivedProductsListView.as_view(), name='archived-products-list'),

    # Список дистрибьюторов
    path('distributors/list/', DistributorListCreateView.as_view(), name='distributor_list_create'),

    # Просмотр/редактирование дистрибьютора
    path('distributors/<int:pk>/', DistributorDetailView.as_view(), name='distributor_detail'),

    # Список архивированных дистрибьюторов
    path('distributors/archive/', DistributorArchiveView.as_view(), name='distributor_archive'),

    path('sales-history/', SalesHistoryListCreateView.as_view(), name='sales-history-list-create'),
    path('sales-history/<int:pk>/', SalesHistoryDetailView.as_view(), name='sales-history-detail'),

    path('return-history/', ReturnHistoryListCreateView.as_view(), name='return-history-list-create'),
    path('return-history/<int:pk>/', ReturnHistoryDetailView.as_view(), name='return-history-detail'),

    # Order URLs
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),

    # Order Item URLs
    path('orders-items/', OrderItemListCreateAPIView.as_view(), name='order-item-list-create'),
    path('orders-items/<int:pk>/', OrderItemRetrieveUpdateDestroyAPIView.as_view(), name='order-item-detail'),

    # Special view to restore stock after order item deletion

]
