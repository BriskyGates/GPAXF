from django.conf.urls import re_path

from App import views

app_name = 'App'

urlpatterns = [
    re_path(r'^home/', views.home, name='home'),
    re_path(r'^market/', views.market, name='market'),   # 点击底部“闪送超市”按钮
    re_path(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params,
        name='market_with_params'),
    re_path(r'^mine/',views.mine,name="mine"),
    re_path(r'^register/',views.register,name="register"),
    re_path(r'^login/',views.login,name="login"),
    re_path(r'^checkuser/',views.check_user),
    re_path(r'^activate/',views.activate),
    re_path(r'^logout/',views.logout,name="logout"),
    re_path(r'^gocart/',views.go_cart,name="cart"),
    re_path(r'^addtocart/',views.add_to_cart),
    re_path(r'^subfromcart/',views.sub_from_cart),
    re_path(r'^addshopping/',views.add_shopping),
    re_path(r'^subshopping/',views.sub_shopping),
    re_path(r'^allselect/',views.cart_all_select),
    re_path(r'^changecartstate/',views.change_cart_state),
    re_path(r'^makeorder/',views.make_order),
    re_path(r'^orderdetail/',views.order_detail),
    re_path(r'^orderlistnotpay/',views.order_not_pay),
    re_path(r'^payed/',views.pay),
    # re_path(r'mail/',views.my_send_email),

]