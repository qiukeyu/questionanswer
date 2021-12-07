function isPhoneNo(phone) {
    var pattern = /^1[34578]\d{9}$/;
    return pattern.test(phone);
}

function formValidate() {
    var str = '';

    // telephone number
    var telephone = $.trim($("#telephone").val())
    if(telephone.length == 0) {
        str += 'phone number can not be none\n';
        $('#telephone').focus();
    } else {
        if(!isPhoneNo(telephone)) {
           str += 'incorrect phone number\n';
           $('#telephone').focus();
        }
    }

    // username
    var username = $("#username").val()
    if(username.length == 0) {
        str += 'username can not be none\n';
        $('#username').focus();
    }

    // password
    var password = $("#password").val()
    if (password.length == 0) {
        str += 'password can not be none\n';
        $('#password').focus();
    } else {
        if( !(password==$("#password2").val()) ) {
           str += 'Entered passwords differ\n';
           $('#password').focus();
        }
    }

    if(str != "") {
        alert(str);
        return false;
    } else {
        $('.auth-form').submit();
    }
}

$('#submit').on('click', function() {
    formValidate();
});