$(document).ready(function(){
    errors = {
        email: '',
        e_conf: '',
        password: '',
        pw_conf: ''
    }
    var reg_email = new RegExp('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')

    function addError(element, type, message) {
        $(element).toggleClass('error', true)
        errors[type] = message
        next = $(element).next('span')
        next.html(message)
        next.css('display', 'block')
    }

    function removeError(element, type) {
        $(element).toggleClass('error', false)
        errors[type] = ''
        next = $(element).next('span')
        next.html('')
        next.css('display', 'none')
    }

    $('#email').blur(function(){
        let email = $(this).val()
        if (!email) {
            addError(this, 'email', 'Email field left blank')
        }
        else if (!reg_email.test(email)) {
            addError(this, 'email', 'Not a valid email')
        }
    })

    $('#email').keyup(function(){
        let email = $(this).val()
        let e_conf = $('#e_conf').val()
        if (reg_email.test(email)) {
            $.ajax({
                url: '/validate_email',
                method: 'POST',
                data: $(this).serialize(),
                success: function(data) {
                    addError('#email', 'email', 'Account already exists')
                },
                error: function() {
                    removeError('#email', 'email')
                }
            })
        }
    })

    $('#e_conf').blur(function(){
        let email = $('#email').val()
        let e_conf = $(this).val()
        if (email != e_conf) {
            addError(this, 'e_conf', 'Email does not match')
        }
    })

    $('#e_conf').keyup(function(){
        let email = $('#email').val()
        let e_conf = $(this).val()
        if (email == e_conf) {
            removeError(this, 'e_conf')
        }
    })

    $('#password').keyup(function(){
        let password = $(this).val()
        let pw_conf = $('#pw_conf').val()
        if (password.length < 6) {
            addError(this, 'password', 'Password must be at least six characters')
        }
        else {
            removeError(this, 'password')
        }
    })

    $('#pw_conf').keyup(function(){
        let password = $('#password').val()
        let pw_conf = $(this).val()
        if (password != pw_conf) {
            addError(this, 'pw_conf', 'Password does not match')
        }
        else {
            removeError(this, 'pw_conf')
        }
    })

    $('#registration').submit(function(){
        for (let error in errors) {
            if (!errors.error){
                return true
            }
            return false
        }
    })
})