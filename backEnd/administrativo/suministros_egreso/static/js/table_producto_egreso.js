
function llenarFila(cantidadS,cantidadD,producto){
    var total=$("#id_productosuministroegreso_set-TOTAL_FORMS").val();
    var bandera=true;
    console.log(cantidadS)
    console.log(cantidadD)
    console.log(producto)
    $("#tableProSum tr").each(function(){
        var hijos=$(this).children();
        var sel=$(hijos[0]).find("select");
        console.log($(sel).val())
        var check=$(hijos[3]).find("input");
        console.log($(check).prop("checked"))
        if($(sel).val()==producto && $(check).prop("checked") == false){
                    bandera=false;
                    $($(hijos[1]).find("input")).val(cantidadS);
                    $($(hijos[2]).find("input")).val(cantidadD);
                    console.log("cambio existente")
        }
    });
    if(bandera){
        console.log("lleno vacia")
        console.log(total)
        $("#id_productosuministroegreso_set-"+(total-2)+"-cantidad_solicitada").val(cantidadS);
        $("#id_productosuministroegreso_set-"+(total-2)+"-cantidad_despachada").val(cantidadD);
        $("#id_productosuministroegreso_set-"+(total-2)+"-producto").val(producto);
    }
}

function borrarFila(producto){
var fila=0;
var total=$("#id_productosuministroegreso_set-TOTAL_FORMS").val()-1;
$("#tableProSum tr").each(function(){
    var pro=$("#id_productosuministroegreso_set-"+fila+"-producto").val();
    if(producto==pro ){
        if(fila!=total){
            $($(this).children()[3]).find("input").prop("checked",true);
        }
    }
    fila=fila+1;
});

}


function cloneMoreMP(selector, prefix) {
    var newElement = $(selector).clone(true);
    
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    var newrow=parseInt(total)+1
    if((parseInt(total)+1)%2==0){
        newrow=2;
    }else{
        newrow=1;
    }
    newElement.attr("class","row"+(newrow) +" form-control pt form-row sumepro_row-productosuministroegreso_set")
    
    var input=newElement.find("input");
    var cont=0;
    $(input).each(function(){
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        
        $(this).attr({'name': name, 'id': id}).removeAttr('checked');
        if($(this).attr("type")=="text"){
            $(this).val("");
        }else if($(this).attr("type")=="hidden"){
            if(cont==0){
                $(this).removeAttr("value");
                cont=1;
            }
            
        }else{
            $(this).val(0);
        }
        
    });


    var select=newElement.find("select");
    $(select).each(function(){
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id});
        $(this).val("");
    });

    var div=newElement.find("div");
    $(div).each(function(){
        if($(this).attr('id')!=undefined){
            var id = $(this).attr('id').replace('-' + (total-1) + '-', '-' + total + '-');
            $(this).attr({'id': id});
        }
        
    });

    var label=newElement.find("label");
    $(label).each(function(){
        var forr = $(this).attr('for').replace('-' + (total-1) + '-', '-' + total + '-');
        $(this).attr({'for': forr});
    });

    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);

}