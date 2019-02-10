from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

LOGIN_REQUIRED_JSON = ["/axf/addtocart/","/axf/subfromcart/","/axf/makeorder/","/axf/changecartstate/","/axf/payed/"]

LOGIN_REQUIRED = ["/axf/gocart/","/axf/orderdetail/","/axf/orderlistnotpay/"]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):
        if request.path in LOGIN_REQUIRED_JSON:
            user_id = request.session.get("user_id")
            if user_id:   # 如果已经登录
                user = AXFUser.objects.get(pk=user_id)
                request.user = user   # 给request对象动态添加一个user属性
            else:   # 未登录
                data = {
                    "status":302,
                }
                request.session["error_message"] = "您还未登录，请先登录！"
                return JsonResponse(data)

        if request.path in LOGIN_REQUIRED:
            user_id = request.session.get("user_id")
            if user_id:  # 如果已经登录
                user = AXFUser.objects.get(pk=user_id)
                request.user = user  # 给request对象动态添加一个user属性
            else:  # 未登录
                request.session["error_message"] = "您还未登录，请先登录！"
                return redirect(reverse("axf:login"))
