$(document).on('click', '#add', function() {
    var extra = $("#codigoe").val();
    localStorage.setItem("codigoevento", extra);

});

$(document).on('click', '#cancelar', function() {
    localStorage.removeItem("codigoevento");

});

$(document).on('click', '#guardar', function() {
    localStorage.removeItem("codigoevento");

});



function load_eventos() {
    console.log("entro a eventos")
    var url = $('#form-fact').attr("data-eventos-url");
    $.ajax({
        url: url,
        success: function(data) {
            console.log(data.eventos);
            $("#codigoe").html(data.eventos);
            if (localStorage.getItem("codigoevento") != null) {
                $("#codigoe").val(localStorage.getItem("codigoevento"));
            }
        }
    });

};

//Para los eventos
load_eventos();


// $(document).on('click', "#codigoe + span", function (e) {
//   load_eventos();
// });