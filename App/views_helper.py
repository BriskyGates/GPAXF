import hashlib

from django.core.mail import send_mail
from django.template import loader


from GPAXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


def send_email_activate(username, receive, u_token):

    subject = '%s AXF Activate' % username

    from_email = EMAIL_HOST_USER   # 从settings.py中获取这个变量，目的是代码与配置分离

    recipient_list = [receive, ]

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/axf/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)
    }

    #  加载激活模板，并传递数据，渲染模板,结果返回的是html代码
    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message="", html_message=html_message, from_email=from_email, recipient_list=recipient_list)


def total_price(carts):
    total = 0.0
    for cart in carts:
        if cart.is_selected:   # 判断该记录是否被选中
            total += cart.goods.price * cart.cart_goods_num

    return "{:.2f}".format(total)




