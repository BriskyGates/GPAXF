from django.db import models

from App.views_constant import ORDER_STATUS_NOT_PAY


class MainModel(models.Model):   # 公共属性抽象到该类中
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class Meta:
        abstract = True   # 设置为抽象模型类


class MainWheel(MainModel):
    class Meta:
        db_table = 'axf_wheel'


class MainNav(MainModel):
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(MainModel):
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(MainModel):
    class Meta:
        db_table = "axf_shop"


class MainShow(MainModel):

    categoryid = models.IntegerField(default=1)
    brandname = models.CharField(max_length=64)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField(default=1)
    productid1 = models.IntegerField(default=1)
    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField(default=1)
    marketprice1 = models.FloatField(default=0)
    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=0)
    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    """
    axf_foodtype(typeid,typename,childtypenames,typesort)
    """

    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    """
    axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,
    childcid,childcidname,dealerid,storenums,productnum) values("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q",
    "","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4)

    """
    productid = models.IntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    pmdesc = models.BooleanField(default=False)
    specifics = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=1)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


class AXFUser(models.Model):
    u_username = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to='icons/%Y/%m/%d/')  # 与MEDIA_ROOT共同决定上传目录
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_user'


# 购物车模型
class Cart(models.Model):
    user = models.ForeignKey(AXFUser,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    cart_goods_num = models.IntegerField(default=1)
    is_selected = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


# 订单模型
class Order(models.Model):
    o_user = models.ForeignKey(AXFUser,on_delete=models.CASCADE)
    o_price = models.FloatField()
    o_time = models.DateTimeField(auto_now=True)
    o_state = models.IntegerField(default=ORDER_STATUS_NOT_PAY)

    class Meta:
        db_table = "axf_orders"


# 订单详情
class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    order_goods_num = models.IntegerField()

    class Meta:
        db_table = "axf_orderdetails"


