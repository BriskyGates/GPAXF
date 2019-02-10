$(function () {

    $(".confirm").click(function () {

        console.log("change state");

        var $confirm = $(this);

        var $li = $confirm.parents("li");

        var cartid = $li.attr('cartid');

        $.getJSON("/axf/changecartstate/", {'cartid': cartid}, function (data) {
            console.log(data);

            if (data['status'] === 200) {
                $("#total_price").html(data['total_price']);
                if (data['c_is_select']) {
                    $confirm.find("span").find("span").html("√");
                } else {
                    $confirm.find("span").find("span").html("");
                }
                if (data['is_all_select']){
                    $(".all_select span span").html("√");
                }else{
                    $(".all_select span span").html("");

                }
            }

        })

    })

    $(".addShopping").click(function () {

        var $add = $(this);

        var $li = $add.parents("li");

        var cartid = $li.attr("cartid");

        $.getJSON("/axf/addshopping/", {"cartid": cartid}, function (data) {
            console.log(data);

            if (data['status'] === 200) {
                 $("#total_price").html(data['total_price']);
                    var $span = $add.prev("span");
                    $span.html(data['c_goods_num']);
            }

        })

    })

    $(".subShopping").click(function(){
        var $sub = $(this);
        var $li = $sub.parents("li");
        var cartid = $li.attr("cartid");
        $.getJSON("/axf/subshopping/",{"cartid":cartid},function(data){
            if (data['status'] === 200) {
                 $("#total_price").html(data['total_price']);
                    var $span = $sub.next("span");
                    if(data["c_goods_num"]>0){
                        $span.html(data['c_goods_num']);
                    }else{
                        $li.remove();    // 在网页上删除当前的购物车条目
                    }
            }
        });
    })

    $(".all_select").click(function () {

        var $all_select = $(this);

        if($all_select.find("span").find("span").html().trim()){
            $all_select.find("span").find("span").html("");
        }else{
            $all_select.find("span").find("span").html("√");
        }

        var unselect_list = [];

        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            if (!($confirm.find("span").find("span").html().trim())) {
                unselect_list.push(cartid);
            }

        })

        if (unselect_list.length > 0) {
            $.getJSON("/axf/allselect/", {"cart_list": unselect_list.join("#")}, function (data) {
                console.log(data);
                if (data['status'] === 200) {
                    $(".confirm").find("span").find("span").html('√');
                    $all_select.find("span").find("span").html("√");
                    $("#total_price").html(data['total_price']);
                }
            })
        }




    })

    $("#make_order").click(function () {

        var select_list = [];

        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid);
            }

        })

        if(select_list.length === 0){
            alert("未选中任何条目，不能下单！");
            return;
        }

        $.getJSON("/axf/makeorder/", function (data) {
            console.log(data);

            if (data['status'] === 200){
                window.open('/axf/orderdetail/?orderid=' + data['order_id'], target="_self");
            }

        })
    })


})