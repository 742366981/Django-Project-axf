from django.shortcuts import render
from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, CartModel, OrderModel, \
    OrderGoodsModel
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse

from utils.functions import get_order_num


def home(request):
    if request.method == 'GET':
        mianwheel = MainWheel.objects.all()
        mainnav = MainNav.objects.all()
        mainmustbuy = MainMustBuy.objects.all()
        mainshop1 = MainShop.objects.all()[0]
        mainshop1_4 = MainShop.objects.all()[1:3]
        mainshop4_8 = MainShop.objects.all()[3:7]
        mainshop7_12 = MainShop.objects.all()[7:11]
        mainshows = MainShow.objects.all()
        data = {
            'mainwheel': mianwheel,
            'mainnav': mainnav,
            'mainmustbuy': mainmustbuy,
            'mainshop1': mainshop1,
            'mainshop1_4': mainshop1_4,
            'mainshop4_8': mainshop4_8,
            'mainshop7_12': mainshop7_12,
            'mainshows': mainshows
        }
        return render(request, 'home/home.html', data)


def market(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:marketparams', kwargs={'typeid': 104749, 'cid': 0, 'sid': 0}))


def marketparams(request, typeid, cid, sid):
    if request.method == 'GET':
        foottypes = FoodType.objects.all()
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid, childcid=cid)

        foodtypes_current = FoodType.objects.filter(typeid=typeid).first()
        childtypes = foodtypes_current.childtypenames
        childtypenames = [x.split(':') for x in childtypes.split('#')]
        if sid == '0':
            pass
        if sid == '1':
            goods = goods.order_by('productnum')
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')
        return render(request, 'market/market.html', {'foottypes': foottypes, 'goods': goods, 'typeid': typeid,
                                                      'childtypenames': childtypenames,
                                                      'cid': cid, 'sid': sid})


def addcart(request):
    if request.method == 'POST':
        user = request.user
        data = {}
        data['code'] = '1001'
        if user.id:
            goods_id = request.POST.get('goods_id')
            cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if cart:
                cart.c_num += 1
                cart.save()
                data['c_num'] = cart.c_num
            else:
                CartModel.objects.create(user=user, goods_id=goods_id, c_num=1)
                data['c_num'] = 1
            data['code'] = '200'
            data['msg'] = '请求成功'
            return JsonResponse(data)
        return JsonResponse(data)


def reducecart(request):
    if request.method == 'POST':
        data = {}
        user = request.user
        if user.id:
            goods_id = request.POST.get('goods_id')
            cart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            if cart.c_num == 1:
                cart.delete()
                data['c_num'] = 0
            else:
                cart.c_num -= 1
                cart.save()
                data['c_num'] = cart.c_num

            return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            carts = CartModel.objects.filter(user=user)
        return render(request, 'cart/cart.html', {'carts': carts})


def changecartstatus(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.get(pk=cart_id)
        if cart.is_select:
            cart.is_select = False
        else:
            cart.is_select = True
        cart.save()
        return JsonResponse({'code': 200, 'is_select': cart.is_select})


def goodscount(request):
    if request.method == 'GET':
        user = request.user
        carts = CartModel.objects.filter(user=user, is_select=True)
        counts_prices = 0
        for cart in carts:
            counts_prices += cart.goods.price * cart.c_num

        counts_prices = '%.2f' % counts_prices
        return JsonResponse({'count': counts_prices, 'code': 200})

def order(request):
    if request.method == 'POST':
        user = request.user
        # 那些商品需要下单
        carts = CartModel.objects.filter(user=user, is_select=True)
        # 创建订单
        o_num = get_order_num()
        order = OrderModel.objects.create(user=user, o_num=o_num)
        # 创建订单详情信息
        for cart in carts:
            OrderGoodsModel.objects.create(order=order,
                                           goods=cart.goods,
                                           goods_num=cart.c_num)
        # 删除购物车中已经下单的商品信息
        carts.delete()

        return JsonResponse({'code': 200, 'order_id': order.id})

def orderInfo(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order_goods = OrderGoodsModel.objects.filter(order_id=order_id)
        return render(request, 'order/order_info.html', {'order_goods': order_goods})

def changeOrderStatus(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()
        order.o_status = 1
        order.save()
        return JsonResponse({'code':200})


def Payed(request):
    if request.method == 'GET':
        user = request.user
        # 待收货
        orders = OrderModel.objects.filter(o_status=1,
                                           user=user)

        return render(request, 'order/order_list_payed.html', {'orders': orders})


def waitPay(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(o_status=0,
                                           user=user)
        return render(request, 'order/order_list_wait_pay.html', {'orders': orders})
