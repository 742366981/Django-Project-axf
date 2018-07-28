from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from app.models import OrderModel
from users.models import UserModel,UserTicketModel
from utils.functions import get_ticket
from datetime import  datetime,timedelta

def my(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        if user.id:
            orders = OrderModel.objects.filter(user=user)
            wait_pay, payed = 0, 0
            for order in orders:
                if order.o_status:
                    payed += 1
                else:
                    wait_pay += 1
            data['payed'] = payed
            data['wait_pay'] = wait_pay

        return render(request, 'mine/mine.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                res = HttpResponseRedirect(reverse('axf:home'))
                out_time = datetime.now() + timedelta(days=1)
                ticket = get_ticket()
                res.set_cookie('ticket', ticket, expires=out_time)
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)

                return res
            else:
                return HttpResponseRedirect(reverse('user:login'))
        else:
            return HttpResponseRedirect(reverse('user:login'))


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        icon = request.FILES.get('icon')
        if password == password2:
            password = make_password(password)
            UserModel.objects.create(username=username, password=password, email=email, icon=icon)
            return HttpResponseRedirect(reverse('user:login'))


def logout(request):
    if request.method == 'GET':
        res = HttpResponseRedirect(reverse('axf:home'))
        res.delete_cookie('ticket')
        return res
