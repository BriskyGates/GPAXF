$(function () {

    var $username = $("#username_input");

    $username.change(function () {
        var username = $(this).val().trim();

        if (username.length) {

            //    将用户名发送给服务器进行预校验
            $.getJSON('/axf/checkuser/', {'username': username}, function (data) {

                console.log(data);

                var $username_info = $("#username_info");

                if (data['status'] === 200){
                    $username_info.html("用户名可用").css("color", 'green');
                }else  if(data['status'] === 901){
                    $username_info.html("用户已存在").css('color', 'red');
                }

            })

        }

    })


})


function check() {
    var $username = $("#username_input");

    var username = $username.val().trim();

    if (!username){
        alert("注册用户名不能为空！");
        return false
    }

    var info_color = $("#username_info").css('color');

    console.log(info_color);

    if (info_color == 'rgb(255, 0, 0)'){
        return false
    }

    var $password_input = $("#password_input");
    var $confirm_password_input = $("#password_confirm_input");

    var password = $password_input.val().trim();
    var confirm_password = $confirm_password_input.val().trim();
    if(password != confirm_password){
        alert("两次输入的密码不一致！");
        return false;
    }

    $password_input.val(md5(password));    //  对密码进行md5加密，放入文本框

    return true
}
