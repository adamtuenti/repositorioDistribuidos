$('.colorMe .tt').each(function() {
    var val = parseInt( $(this).text(), 10),
    if (val < 80) {
        $(this).css('background-color', 'red');
    }
});