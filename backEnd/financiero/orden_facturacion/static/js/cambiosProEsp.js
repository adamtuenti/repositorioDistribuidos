$("#descmeme").children().each(function() {
    var primerc = $(this).children()[0];
    cedula = $(primerc).html().split(" ")[0];
    var evento=$($(this).children()[1]).html();

    var url = $('#form-fact').attr("data-partproesp-url");
    $.ajax({
        url: url,
        data: {
            'cedula': cedula,
            "codigo": evento,
        },
        success: function(data) {
            if (data.bandera) {
                $("#be"+data.cedula+data.codigo).prop("hidden", true);
            }
        }
    });

});