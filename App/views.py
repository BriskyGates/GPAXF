import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from App.models import *
from App.views_constant import *
from App.views_helper import send_email_activate, total_price
from GPAXF.settings import MEDIA_KEY_PREFIX


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys= MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    print("mainshop0_1的类型",type(main_shop0_1))
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.objects.all()
    title = "首页"
    return render(request,'main/home.html',locals())


def market(request):#点击闪送超市后,该视图函数进行处理
    return redirect(reverse("axf:market_with_params",
                            kwargs={"typeid":"104749","childcid":"0","order_rule":"0"}))


def market_with_params(request, typeid, childcid, order_rule):
    foodtypes =FoodType.objects.all()
    foodtype = FoodType.objects.get(typeid=typeid)   # 根据大类型标识查询某个类型记录
    childtypenames = foodtype.childtypenames   # 获取当前大类型对应的小类型字符串
    child_list = childtypenames.split("#")  # 拆分结果，形如：“['全部分类:0', '杂粮米面油:103570', '厨房调味:103571', '调味酱:103572']”
    foodtype_childname_list = []
    for child in child_list:
        foodtype_childname_list.append(child.split(":"))  # 大列表套着小列表，小列表有两个元素，第一个是子类型名称，第二个是子类标识

    goods_list = Goods.objects.filter(categoryid=typeid)   # 通过大类型的id查询对应的商品
    if childcid == ALL_TYPE:    # 如果商品的子类型是“全部分类”
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)   # QuerySet调用filter(),筛选子种类（小种类）商品

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    order_rule_list = [
        ["综合排序",ORDER_TOTAL],
        ["价格升序", ORDER_PRICE_UP],
        ["价格降序", ORDER_PRICE_DOWN],
        ["销量升序", ORDER_SALE_UP],
        ["销量降序", ORDER_SALE_DOWN],
    ]

    user_id = request.session.get("user_id")
    if user_id:  # 如果已登录
        user = AXFUser.objects.get(pk=user_id)
        user_carts = Cart.objects.filter(user=user)  # 查询当前用户的购物车记录
        for goods in goods_list:
            carts = user_carts.filter(goods=goods)
            if carts.exists():
               cart = carts.first()  # 查询当前用户对当前遍历商品的购物车记录
               goods.cart_goods_num = cart.cart_goods_num
               # 动态添加商品的cart_goods_num属性

    data = {
        "foodtypes":foodtypes,
        "typeid":int(typeid),
        "childcid":childcid,
        "goods_list":goods_list,
        "foodtype_childname_list":foodtype_childname_list,
        "order_rule_list":order_rule_list,
        "order_rule_view":order_rule,
        "title":"闪送超市",
    }
    return render(request,'main/market.html',data)


def mine(request):
    user_id = request.session.get("user_id")
    data = {
        "title":"我的",
        "is_login":False
    }
    if user_id:   # 如果已经登录
        user = AXFUser.objects.get(pk=user_id)  # 根据用户id查询用户
        data["icon"] = MEDIA_KEY_PREFIX + user.u_icon.name
        data["is_login"] = True
        data["username"] = user.u_username
        # 当前用户订单状态为未支付的订单个数
        data["order_not_pay"] = Order.objects.filter(o_user=user).filter(o_state=ORDER_STATUS_NOT_PAY).count()
        # 当前用户订单状态为待收货的个数
        data["order_not_receive"] = Order.objects.filter(o_user=user).filter(o_state__in=[ORDER_STATUS_NOT_SEND,ORDER_STATUS_NOT_RECEIVE]).count()

    return render(request,'main/mine.html',data)


def check_user(request):
    username = request.GET.get("username")  # 接收注册页面上Ajax传递的用户名
    print("接收到的用户名是："+username)
    users = AXFUser.objects.filter(u_username=username)
    data = {
        "status":200,
    }
    if users.exists():
        data["status"] = 901

    return JsonResponse(data)


# 注册
def register(request):
    if request.method == "GET":
        return render(request,'user/register.html',{"title":"注册"})
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("接收到的密码是："+password)
        icon = request.FILES.get("icon")   # 接收上传的图片
        new_user = AXFUser()
        new_user.u_username = username
        your_password = make_password(password)  # 密码加密
        new_user.u_password = your_password
        new_user.u_email = email
        new_user.u_icon = icon
        new_user.save()   # 存入数据库

        u_token = uuid.uuid4().hex   # 生成一个随机字符串
        cache.set(u_token,new_user.id,timeout=60*60*24)  # 将用户id存入缓存
        send_email_activate(username,email,u_token)   # 发送激活邮件
        return redirect(reverse("axf:login"))


def login(request):
    if request.method == "GET":
        error_message = request.session.get("error_message")  # 获取错误信息
        data = {
            "title": "登录",
        }
        if error_message:    # 如果session中存在错误消息
            del request.session["error_message"]   # 删除session中的错误提示
            data["error_message"] = error_message

        return render(request, 'user/login.html',data)
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        users = AXFUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()
            if check_password(password,user.u_password):
                if user.is_active:    # 判断是否被激活
                    request.session["user_id"] = user.id    #  将用户id存入session
                    return redirect(reverse("axf:mine"))
                else:
                    request.session["error_message"] = "用户未激活！"
                    return redirect(reverse("axf:login"))
            else:
                request.session["error_message"] = "密码错误！"
                return redirect(reverse("axf:login"))
        else:
            request.session["error_message"] = "该用户不存在！"
            return redirect(reverse("axf:login"))


# 登出
def logout(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))


# 激活，点击邮件中的“激活”超链接调用此函数
def activate(request):
    u_token = request.GET.get("u_token")   # 接收“激活”超链接中传递过来的参数
    user_id = cache.get(u_token)   # 从缓冲中获取用户id
    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True   #  将用户的激活状态改为True
        user.save()   # 更改
        return redirect(reverse("axf:login"))

    return render(request,'user/activate_fail.html')


def go_cart(request):
    carts = Cart.objects.filter(user=request.user)   # 查询出当前用户的所有购物车记录
    data = {
        "title":"购物车",
        "carts":carts,
        "total_price":total_price(carts)
    }
    return render(request,'main/cart.html',data)


# 添加到购物车
def add_to_cart(request):
    goodsid = request.GET.get("goodsid")   # 接收附加在按钮上的商品id
    carts = Cart.objects.filter(user=request.user).filter(goods_id=goodsid)
    if carts:   # 已经存在购物车记录
        cart = carts.first()   # 获取购物车对象
        cart.cart_goods_num = cart.cart_goods_num + 1
    else:
        cart = Cart()
        cart.user = request.user
        cart.goods_id = goodsid
        cart.cart_goods_num = 1

    cart.save()   # 保存或更新
    data = {
        "status":200,
        "c_goods_num":cart.cart_goods_num,
    }
    return JsonResponse(data)


# 从购物车中减去商品
def sub_from_cart(request):
    goodsid = request.GET.get("goodsid")  # 接收附加在按钮上的商品id
    carts = Cart.objects.filter(user=request.user).filter(goods_id=goodsid)
    cart = carts.first()

    data = {
        "status": 200,
    }

    if cart.cart_goods_num > 1:
        cart.cart_goods_num = cart.cart_goods_num - 1   # 购物车中该商品的数量减一
        cart.save()
        data["c_goods_num"] = cart.cart_goods_num
    else:   #  如果该商品在购物车中只有一个
        cart.delete()  # 删除该条购物车记录
        data["c_goods_num"] = 0

    return JsonResponse(data)


def add_shopping(request):   # 在购物车页面点击“加号”按钮
    cartid = request.GET.get("cartid")   # 获取购物车id
    cart = Cart.objects.get(pk=cartid)
    cart.cart_goods_num = cart.cart_goods_num + 1
    cart.save()

    user_id = request.session.get("user_id")
    user = AXFUser.objects.get(pk=user_id)
    carts = Cart.objects.filter(user=user)  # 查询出当前用户的所有购物车记录
    totalprice = total_price(carts)

    data = {
        "status":200,
        "total_price":totalprice,
        "c_goods_num":cart.cart_goods_num,
    }
    return JsonResponse(data)



def sub_shopping(request):   # 在购物车页面点击“减号”按钮
    cartid = request.GET.get("cartid")   # 获取购物车id
    cart = Cart.objects.get(pk=cartid)
    cart.cart_goods_num = cart.cart_goods_num - 1
    cart.save()
    if cart.cart_goods_num == 0:   # 如果购物车的该商品数量为0
        cart.delete()   # 删除数据库表中的记录

    user_id = request.session.get("user_id")
    user = AXFUser.objects.get(pk=user_id)
    carts = Cart.objects.filter(user=user)  # 查询出当前用户的所有购物车记录
    totalprice = total_price(carts)

    data = {
        "status": 200,
        "total_price": totalprice,
        "c_goods_num":cart.cart_goods_num
    }

    return JsonResponse(data)


def cart_all_select(request):     # 在购物车页面点击全选
    unselected = request.GET.get("cart_list")

    if unselected:
        unselected_list = unselected.split("#")
        for cartid in unselected_list:
            cart = Cart.objects.get(pk=cartid)
            cart.is_selected = True
            cart.save()

    user_id = request.session.get("user_id")
    user = AXFUser.objects.get(pk=user_id)
    carts = Cart.objects.filter(user=user)  # 查询出当前用户的所有购物车记录
    totalprice = total_price(carts)

    data = {
        "status":200,
        "total_price":totalprice
    }
    return JsonResponse(data)


def change_cart_state(request):   #  在购物车页面点击购物车条目的选中状态
    cartid = request.GET.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.is_selected = not cart.is_selected   #  状态取反
    cart.save()   # 更新该条购物车记录

    carts = Cart.objects.filter(user=request.user)  # 查询出当前用户的所有购物车记录
    is_all_select = True
    for c in carts:
        if not c.is_selected:
            is_all_select = False
            break

    data = {
        "status": 200,
        "c_is_select": cart.is_selected,
        "total_price":total_price(carts),
        "is_all_select":is_all_select
    }
    return JsonResponse(data)


# 下单
def make_order(request):
    order = Order()   # 实例化订单对象
    order.o_user = request.user
    carts = Cart.objects.filter(user=request.user).filter(is_selected=True)  # 查询当前用户的购物车记录
    order.o_price = total_price(carts)
    order.save()  # 保存到数据库

    for cart in carts:
        orderdetail = OrderDetail()   # 每个购物车记录对应一个订单详情信息
        orderdetail.order = order
        orderdetail.goods = cart.goods
        orderdetail.order_goods_num = cart.cart_goods_num
        orderdetail.save()  # 保存订单详情
        cart.delete()   #  删除当前遍历的购物车记录

    data = {
        "status":200,
        "order_id":order.id
    }
    return JsonResponse(data)


# 显示订单详情页面
def order_detail(request):
    orderid = request.GET.get("orderid")   # 接收刚刚下单的订单id
    order = Order.objects.get(pk=orderid)
    data = {
        "title":"订单详情",
        "order":order
    }
    return render(request,'order/order_detail.html',data)


def order_not_pay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_state=ORDER_STATUS_NOT_PAY)
    data = {
        "title":"未支付订单",
        "orders":orders
    }

    return render(request,'order/order_list_not_pay.html',data)


def pay(request):
    orderid = request.GET.get("orderid")
    order = Order.objects.get(pk=orderid)
    order.o_state = ORDER_STATUS_NOT_SEND   # 修改为已支付状态
    order.save()
    data = {
        "status":200
    }
    return JsonResponse(data)




















# def my_send_email(request):
#     subject = "好好学习吧！"
#     message = "<h3>Come on~~~</h3>"
#     from_email = '15114855862@163.com'
#     receive_list = ['15114855862@163.com',]
#     send_mail(subject=subject,message=message,from_email=from_email,recipient_list=receive_list,
#               html_message=message)
#     return HttpResponse("邮件发送成功！")


