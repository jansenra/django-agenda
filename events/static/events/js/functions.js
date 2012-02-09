$(function() {
    $('a.view_events').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('div.events-outline').load($(this).attr('href'));
    })

    $('div.event-detail a.rsvp').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('#rsvp_form input[name=rsvp]').val($(this).attr('rsvp'));
        $('#rsvp_form').submit();
    });
});
