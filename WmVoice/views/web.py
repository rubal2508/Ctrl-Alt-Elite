import operator
from functools import reduce
from django.db.models import Q
from django.views import View
from django.shortcuts import render, redirect
from WmVoice.constants import COMMA_SEPARATOR
from WmVoice.models import Item, User, ItemOrder
from hashlib import sha256


def setUser(request, user):
    request.session['user_id'] = user.id


def getUser(request):
    try:
        return User.objects.get(id=request.session.get('user_id'))
    except Exception:
        return None


def removeUserFromSession(request):
    del request.session['user_id']


class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name='WmVoice/home.html',
            context={
                'user': getUser(request),
            }
        )

    def post(self, request):
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        message = None

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.password == sha256(password.encode('utf-8')).hexdigest():
                setUser(request, user)
            else:
                message = "Invalid password"
        else:
            message = "Invalid Email address"

        return render(
            request,
            template_name='WmVoice/home.html',
            context={
                'user': getUser(request),
                'message': message,
            }
        )


class LogoutView(View):

    def get(self, request):
        removeUserFromSession(request)
        return redirect('home')


class SearchView(View):

    def fetchItems(self, searchQ):
        queryStrings = [queryString.strip().replace('"', '').replace("'", "")
                        for queryString in searchQ.strip().split(COMMA_SEPARATOR)]

        # Filter via name
        name_check_condition = reduce(
            operator.or_, [Q(name__contains=s) for s in queryStrings])
        items = Item.objects.filter(name_check_condition)
        return items

    def get(self, request):
        searchQ = request.GET.get('q')
        items = self.fetchItems(searchQ)
        return render(
            request,
            template_name='WmVoice/search.html',
            context={
                'searchQ': searchQ,
                'items': items,
                'user': getUser(request),
            }
        )


class ItemView(View):

    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        return render(
            request,
            template_name='WmVoice/item.html',
            context={
                'item': item,
                'user': getUser(request),
            }
        )


class OrderView(View):

    def get(self, request):
        user = getUser(request)
        return render(
            request,
            template_name='WmVoice/orders.html',
            context={
                'user': user,
            }
        )


class SingleOrderView(View):

    def get(self, request, order_id):
        user = getUser(request)
        return render(
            request,
            template_name='WmVoice/order.html',
            context={
                'user': user,
                'order': ItemOrder.objects.get(id=order_id),
            }
        )
