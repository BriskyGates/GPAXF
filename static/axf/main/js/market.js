$(function () {

    $("#all_types").click(function () {

        console.log("全部类型");

        var $all_types_container = $("#all_types_container");

        $all_types_container.show();

        var $all_type = $(this);

        var $span = $all_type.find("span").find("span");

        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        var $sort_rule_container = $("#sort_rule_container");

        $sort_rule_container.slideUp();

        var $sort_rule = $("#sort_rule");

        var $span_sort_rule = $sort_rule.find("span").find("span");

        $span_sort_rule.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#all_types_container").click(function () {

        var $all_type_container = $(this);

        $all_type_container.hide();

        var $all_type = $("#all_types");

        var $span = $all_type.find("span").find("span");

        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })


    $("#sort_rule").click(function () {

        console.log("排序规则");

        var $sort_rule_container = $("#sort_rule_container");

        $sort_rule_container.slideDown();

        var $sort_rule = $(this);

        var $span = $sort_rule.find("span").find("span");

        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        var $all_type_container = $("#all_types_container");

        $all_type_container.hide();

        var $all_type = $("#all_types");

        var $span_all_type = $all_type.find("span").find("span");

        $span_all_type.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");


    })

    $("#sort_rule_container").click(function () {

        var $sort_rule_container = $(this);

        $sort_rule_container.slideUp();

        var $sort_rule = $("#sort_rule");

        var $span = $sort_rule.find("span").find("span");

        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })


    $(".subShopping").click(function () {
        var $sub_button = $(this);
        var span_num = $sub_button.next("span").html();
        if(span_num == "0"){
            alert("购物车中本无此商品！");
            return;    // 结束函数的执行
        }
        var goodsid = $sub_button.attr('goodsid');

        $.get('/axf/subfromcart/', {'goodsid': goodsid}, function (data) {
            console.log(data);

            if (data['status'] === 302){
                window.open('/axf/login/', target="_self");
            }else if(data['status'] === 200){
                $sub_button.next('span').html(data['c_goods_num']);   // 将减按钮紧邻后面的（同辈）元素中的内容设置为商品在购物车中的数量
            }

        })



        // var goodsid = $add.attr("goodsid");
        // var goodsid = $add.prop("goodsid");
        //
    })

    $(".addShopping").click(function () {
        var $add = $(this);

        var goodsid = $add.attr('goodsid');

        $.get('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);

            if (data['status'] === 302){
                window.open('/axf/login/', target="_self");
            }else if(data['status'] === 200){
                $add.prev('span').html(data['c_goods_num']);   // 将添加按钮前面的（同辈）元素中的内容设置为商品在购物车中的数量
            }

        })

    })

})