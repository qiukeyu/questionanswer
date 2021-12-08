if (typeof(Storage) !== "undefined") {
    var telephone=document.querySelector('#user-telephone');
    var password=document.querySelector('#user-password');
    var check=document.querySelector('#check');
    var button=document.querySelector('button');

    button.onclick=function(){
        if(check.checked){
            window.localStorage.setItem('telephone', telephone.value);
            window.localStorage.setItem('password', password.value);
        }else{
            window.localStorage.removeItem('telephone');
            window.localStorage.removeItem('password');
        }
    }
    window.onload=function() {
        document.getElementById("user-telephone").value = localStorage.getItem("telephone");
        document.getElementById("user-password").value = localStorage.getItem("password");
    }
}