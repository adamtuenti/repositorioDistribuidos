$(document).ready(function () {
    var todas_filas = $('table tr');
    todas_filas.each(function(index,element){
        var codigos_vistos = []
        var fila = todas_filas[index];
        
        var celda_codigos = $(fila).find($('td#td_codigos_eventos span'));
        var celda_nombres = $(fila).find($('td#td_nombres_eventos span'));
        
        $(celda_codigos).each(function (index, element) {
            var c = $(element).html()
            if(codigos_vistos.indexOf(c)== -1){
                codigos_vistos.push(c);
            }
            else{
                $(celda_codigos[index]).remove();
                $(celda_nombres[index]).remove();
            }
        });
    });
});