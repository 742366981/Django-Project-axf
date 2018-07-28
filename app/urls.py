"""axf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^home/', views.home,name='home'),
    url(r'^market/', views.market,name='market'),
    url('marketparams/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sid>\d+)/',views.marketparams,name='marketparams'),
    url(r'addcart/',views.addcart),
    url(r'reducecart/',views.reducecart),
    url(r'cart/',views.cart,name='cart'),
    url(r'changecartstatus/',views.changecartstatus),
    url(r'goodscount/',views.goodscount),
    url(r'order/', views.order, name='order'),
    url(r'orderInfo/', views.orderInfo, name='orderInfo'),
    # 修改订单的状态
    url(r'changeOrderStatus/', views.changeOrderStatus, name='changeOrderStatus'),
    # 待收货
    url(r'payed/', views.Payed, name='payed'),
    # 待支付
    url(r'waitPay/', views.waitPay, name='waitPay'),
]
