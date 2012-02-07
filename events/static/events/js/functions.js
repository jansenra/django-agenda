$(function() {
    $('div.events-calendar a.view_events').click(function(e) {
        e.stopPropagation();
        e.preventDefault();
        console.log($(this).attr('href'));
        $('div.events div.events-outline').load($(this).attr('href'));
    })
});
