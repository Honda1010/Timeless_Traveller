let register_button = document.getElementById('Register_button');
let back_to_login = document.getElementById('back_to_login');

register_button.addEventListener('click', function () {
    window.location.href = '../templates/Registration.html'; 
});

back_to_login.addEventListener('click',function(event){
    window.location.href = '../templates/login.html'; 
});
