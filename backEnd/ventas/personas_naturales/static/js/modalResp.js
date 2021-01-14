
// cont =0;
// $(function() {
    
//     $("#form-segNat").submit(function(event) {
//         // Stop form from submitting normally
//         event.preventDefault();
//         var friendForm = $(this);
//         // Send the data using post
//         var posting = $.post( friendForm.attr('action'), friendForm.serialize() );
//         $('#seguimientoNatural').modal('toggle');
//         // if success:
//         posting.done(function(data) {
//             console.log("se hizo el post");
//             $('#seguimiento_exito').modal('toggle');
//         });
//         // if failure:
//         posting.fail(function(data) {
//             // 4xx or 5xx response, alert user about failure
//             $("#listaErrores li").remove();
//             console.log("fallo el post");
//             console.log($("#id_cod_evento").val())
//                 if($("#id_cod_evento").val()==""){
//                     var elemento=$("<li>");
//                     var elemento2=$("<li>");
//                     elemento.html("Falto agregar Código del Evento");
//                     elemento2.html("Falto agregar Nombre del Evento");
//                     $("#listaErrores").append(elemento);
//                     $("#listaErrores").append(elemento2);
//                 }
    
//                 var finico=new Date($("#id_fecha_registro").val());
//                 var fsegumiento=new Date($("#id_fecha_seguimiento").val());
//                 var fproximo=new Date($("#id_proximo_seguimiento").val());
    
    
//                 if(addDays(finico,15)>fsegumiento){
//                     var elemento3=$("<li>");
//                     elemento3.html("La fecha de seguimiento puede ser hasta 15 dias menor a la fecha de registro");
//                     $("#listaErrores").append(elemento3);
//                 }
    
//                 if(addDays(finico,15)>fproximo){
//                     var elemento4=$("<li>");
//                     elemento4.html("La fecha de proximo seguimiento puede ser hasta 15 dias menor a la fecha de registro");
//                     $("#listaErrores").append(elemento4);
//                 }
    
//                 if(fsegumiento>=fproximo){
//                     var elemento5=$("<li>");
//                     elemento5.html("La fecha de proximo seguimiento no debe ser menor o igual a la fecha de mayor seguimiento");
//                     $("#listaErrores").append(elemento5);
//                 }
                
//             $('#seguimiento_fallida').modal('toggle');
//         });
//     });
// });

// function addDays(date, days) {
//     var result = new Date(date);
//     result.setDate(result.getDate() - days);
//     return result;
//   }

$(document).on('submit',"#form-segNat",function(e){
    // Stop form from submitting normally
    e.preventDefault();
    var myform = $(this);
    console.log(myform)
    var url=myform.attr("action");
    $.ajax({
        type: 'POST',
        url: url,
        data: myform.serialize(),
        dataType: 'json',
        success: function (response) {
           // myform.trigger('reset')
            // $("#personaModal").modal('hide');
            // var content=$("<div>");
            // var span=$("<span>");
            // span.html(response.msj);
            // content.append(span);
            // $("#respuesta-post .modal-body").html(content);
            // $("#respuesta-post").modal('show');
            $('#seguimientoNatural').modal('toggle');
            $('#seguimiento_exito').modal('toggle');
        },
        error: function (response) {
            $("#modal-content-seguimiento").html(response["responseText"])
            // init_all();
        }
    });
})

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