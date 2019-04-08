$(document).ready(function(){
    errors = true

    $('#login').submit(function(){
        if (errors) {
            $('#password').next('span').html('Invalid Username or Password')
            $('#password').next('span').css('display', 'block')
        }
    })
})