$(document).ready(function(){
    //variables
    pageId = window.location.pathname.split('/').pop()

    //mobile switching
    $('#nav-players').click(function(){
        $('.widget').css('z-index', '0')
        $('#players').css('z-index', '100')
    })
    $('#nav-updates').click(function(){
        $('.widget').css('z-index', '0')
        $('#updates').css('z-index', '100')
    })
    $('#nav-chat').click(function(){
        $('.widget').css('z-index', '0')
        $('#chat').css('z-index', '100')
    })
    
    //players
    error = true
    
    $('p.first').click(function(){
        $(this).siblings('.character').slideToggle(200)
    })
    
    $('#search').keyup(function(){
        if ($(this).val().length > 5) {
            $.ajax({
                url: '/validate/' + pageId + '/user',
                method: 'GET',
                data: $(this).serialize(),
                success: function(data) {
                    $('#search').css('box-shadow', '0 0 4px 2px green')
                    $('#form-add-user-submit').css('background-color', 'black')
                    $('#form-add-user-submit').css('cursor', 'pointer')
                    error = false
                },
                error: function() {
                    $('#search').css('box-shadow', 'none')
                    $('#form-add-user-submit').css('background-color', 'grey')
                    $('#form-add-user-submit').css('cursor', 'default')
                    error = true
                }
            })
        }
        else {
            $('#search').css('box-shadow', 'none')
            $('#form-add-user-submit').css('background-color', 'grey')
            error = true
        }
    })

    $('#form-add-user').submit(function(){
        if (!error) {
            $.ajax({
                url: '/campaign/' + pageId + '/addplayer',
                method: 'POST',
                data: $('#search').serialize(),
                success: function(data){
                    $('#player-list').append('<p>' + data + '</p>')
                    $('#search').val('')
                }
            })
        }
        return false
    })

    //characters
    $('#form-add-character').submit(function(){
        if ($('#name').val().length > 0 && $('#race').val().length > 0 && $('#class').val().length > 0) {
            console.log('clicked!')
            $.ajax({
                url: '/addcharacter',
                method: 'POST',
                data: $('#form-add-character').serialize(),
                success: function(data){
                    console.log(data)
                }
            })
        }
        return false
    })
})