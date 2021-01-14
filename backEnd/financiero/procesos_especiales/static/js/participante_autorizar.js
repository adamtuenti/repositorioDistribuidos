


function llenar_tabla(){
    $("#tablePart tr").each(function(){
        var row=$("<tr>");
        row.attr("class","text-center");
        var participante=$("<td>");
        var nombre_evento=$("<td>");
        var codigo=$("<td>");
        var descuento=$("<td>");
        var valor=$("<td>");
        var acciones=$("<td>");
    
        row.append(participante);
        row.append(nombre_evento);
        row.append(codigo);
        row.append(descuento);
        row.append(valor);
        row.append(acciones);
    
        var primer=$(this).children()[0]
        var pselect=$(primer).find("select");
        console.log(pselect);
        console.log($(pselect).val());
        $(pselect).children().each(function(){
            if($(this).val()==$(pselect).val()){
                participante.html($(this).text());
            }
        });
    
        var segundo=$(this).children()[1]
        var sinput=$(segundo).find("input");
        nombre_evento.html($(sinput).val());
    
        var tercer=$(this).children()[2]
        var tinput=$(tercer).find("input");
        codigo.html($(tinput).val());
    
        var cuart=$(this).children()[4]
        var cinput=$(cuart).find("input");
        descuento.html("%"+$(cinput).val());
    
        var quinto=$(this).children()[5]
        var qinput=$(quinto).find("input");
        //valor.html($(qinput).val());
        valor.html("$ " + formatNumber($(qinput).val()));
        

        var last=$(this).children()[6]
        var clast=$(last).find("input");

        if($(sinput).val()!="" && !($(clast).prop("checked")==true)){
            $("#tbodyPart").append(row);
        }
    
    });

    $("#id_n_participantes").val($("#tbodyPart").children().length);
}

llenar_tabla();


$(document).on('click','.eliminarRow',function(){
    console.log(this)
    var tr=$(this).parent().parent();
    console.log(tr)
    var children=$(tr).children();
    console.log(children);

    var codigo= $(children[2]).html();
    console.log(codigo);

    var participante=$(children[0]).html();
    var cedula=participante.split(" ")[0];
    console.log(cedula);

    $("#tablePart tr").each(function(){
        
        var primer=$(this).children()[0]
        var pselect=$(primer).find("select");
        
        var tercer=$(this).children()[2]
        var tinput=$(tercer).find("input");

        if($(pselect).val()==cedula && $(tinput).val()==codigo){
            var last=$(this).children()[6]
            var clast=$(last).find("input");
            $(clast).prop("checked", true);
        }

    });

    $(tr).remove();
    calcular();
});

$(document).on('click', '#MEGAHACK', function () {
    cloneMore('.pt:last', 'procesoparticipante_set');
});   

$(document).on('actualizar', '#MEGAHACK', function () {
    $("#tbodyPart").children().each(function(){
        $(this).remove();
    });
    llenar_tabla();
    calcular();
});  

function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    var newrow=parseInt(total)+1
    if((parseInt(total)+1)%2==0){
        newrow=2;
    }else{
        newrow=1;
    }
    newElement.attr("class","row"+(newrow) +" form-control pt form-row participantesPE_row-procesoparticipante_set")
    
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




function calcular(){
    var subtotal=0;
    var descuentos=0;
    var descuentoTotal=0;
    var valorTotal=0;
    $("#tablePart tr").each(function(){
        
        var segundo=$(this).children()[1]
        var sinput=$(segundo).find("input");

        var tercer=$(this).children()[3]
        var tinput=$(tercer).find("input");
    
        var cuart=$(this).children()[4]
        var cinput=$(cuart).find("input");
        

        var quinto=$(this).children()[5]
        var qinput=$(quinto).find("input");


        var last=$(this).children()[6]
        var clast=$(last).find("input");

        if($(sinput).val()!="" && !($(clast).prop("checked")==true)){
            subtotal=subtotal+parseInt($(tinput).val());
            valorTotal=valorTotal+parseInt($(qinput).val());
        }
    });

    descuentoTotal=subtotal-valorTotal;
    descuentos=((100*descuentoTotal)/subtotal).toFixed(2);
    // $("#subtotal").val(subtotal);
    // $("#descuento_fact").val(descuentos);
    // $("#descuento_total").val(descuentoTotal);
    // $("#valor_total").val(valorTotal);

    $("#subtotal").val(formatNumber(subtotal));
    $("#descuento_fact").val(descuentos);
    $("#descuento_total").val(formatNumber(descuentoTotal));
    $("#valor_total").val(formatNumber(valorTotal));

    $("#id_subtotal").val(subtotal);
    $("#id_descuento_fact").val(descuentos);
    $("#id_descuento_total").val(descuentoTotal);
    $("#id_valor_total").val(valorTotal);

}

calcular();

//Bloquear campos
$("#id_categoria").prop("disabled",true);
$("#id_concepto").prop("disabled",true);
$("#codigoEvento").prop("disabled",true);
$("#id_descuentoC").prop("disabled",true);
