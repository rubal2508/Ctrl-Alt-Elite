from django.urls import path
from WmVoice.views import web

urlpatterns = [
    path('', web.HomeView.as_view(), name='home'),
    path('logout', web.LogoutView.as_view(), name='logout'),
    path('search', web.SearchView.as_view(), name='search'),
    path('items/<int:item_id>', web.ItemView.as_view(), name='item'),
    path('orders', web.OrderView.as_view(), name='orders'),
    path('order/<int:order_id>', web.SingleOrderView.as_view(), name='order'),
]
