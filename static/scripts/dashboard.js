$(document).ready(function(){
    $('.new').click(function(){
        $(this).after(`
        <div id="campaign-form">
            <form action="/campaigns/create" method="post">
                <h2>New Campaign</h2>
                <input type="text" name="name" placeholder="Campaign Name">
                <button type="submit">Create</button>
                <button type="button" class="cancel">Cancel</button>
            </form>
        </div>
        `)
    })
    $('.campaigns').on('click', 'button.cancel', function(){
        $('#campaign-form').remove()
    })
})