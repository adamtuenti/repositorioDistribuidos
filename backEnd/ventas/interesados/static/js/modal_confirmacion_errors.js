
cont =0;
$(function() {
    
    $("#form-seguimiento-interesado").submit(function(event) {
        // Stop form from submitting normally
        event.preventDefault();
        var friendForm = $(this);
        // Send the data using post
        var posting = $.post( friendForm.attr('action'), friendForm.serialize() );
        // if success:
        posting.done(function(data) {
            $('#seguimientoInteresado').modal('toggle');
            $('#seguimiento_exito').modal('toggle');
        });
        // if failure:
        posting.fail(function(response) {
             $("#seguimientoInteresado .modal-content").html(response["responseText"]);                                                                                                                                                                                       

        });
    });
});

/**
 * Function to setup an ajax post. Useful to display form with errors when the server responses
 */
$(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
