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
window.onload=function(){
    telephone.value=window.localStorage.getItem('userName');
    password.value=window.localStorage.getItem('pwd');
}