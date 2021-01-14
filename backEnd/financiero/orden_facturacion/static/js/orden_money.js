var p_url = "";

    $('#id_participante').select2({
        minimumInputLength: 2,
        language: {
            noResults: function () {
                $(".select2-results__options").append("<a id='pnuevo' class='btn btn-secondary btn-block btn-sm' href='{% url 'natural_nuevo' %}' target='_blank'>Agregar Nuevo</a>");
                return "No hay resultados";
            },
            searching: function () {

                return "Buscando...";
            },
            inputTooShort: function (e) {
                var t = e.minimum - e.input.length;
                return "Ingresa " + t + " caractéres para buscar";
            }
        }
    });

    

    calcular();

    $('#id_valor_evento').change(function (e) {
        calcular();
    });

    $('#id_descuento').change(function (e) {
        back($('#id_valor_evento'));
        calcular();
        transform($('#id_valor_evento'));
        transform($("#id_valor"));
    });

    function roundToTwo(num) {
        return +(Math.round(num + "e+2") + "e-2");
    }
    function calcular() {
        var v_evento = $('#id_valor_evento').val();
        var desc = $("#id_descuento").val();

        if (v_evento == null || v_evento <= 0) {
            $("#id_valor").val(0.0);
            v_evento = 0;
        }
        if (desc == null || desc <= 0) {
            desc = 0;
        }
        desc = 1 - (desc / 100);
        v_evento *= desc;
        $("#id_valor").val(roundToTwo(v_evento));
        
    }

//Cambiar el signo de dolar
var valor=$("#div_id_valor_evento");
var inp=$("#div_id_valor_evento input");
var hijos=valor.children();
const dnuevo=hijos[1];
dnuevo.remove();
const dollar=$("<div>");
dollar.attr("class","input-icon")
const icono=$("<i>");
icono.text("$");
dollar.append(inp);
dollar.append(icono);
valor.append(dollar);

//Cambiar el signo de dolar
var valor2=$("#div_id_valor");
var inp2=$("#div_id_valor input");
var hijos2=valor2.children();
const dnuevo2=hijos2[1];
dnuevo2.remove();
const dollar2=$("<div>");
dollar2.attr("class","input-icon")
const icono2=$("<i>");
icono2.text("$");
dollar2.append(inp2);
dollar2.append(icono2);
valor2.append(dollar2);

console.log("jeje")

  if($("#id_valor_evento").val()!=""){
    transform($("#id_valor_evento"));
  }

  if($("#id_valor").val()!=""){
    transform($("#id_valor"));
  }

  


function back(input){
    const val=$(input).val();
    $(input).attr("type","number");
    $(input).val(parseFloat(val.replace(/,/g,"")));
    $(input).val(parseFloat($(input).val()).toFixed(2));
}

//Funcion para establecer Formato de Dinero
function transform(input){
    if($(input).val()!=""){
      $(input).val(parseFloat($(input).val()).toFixed(2));
    $(input).attr("type","text");
    var numeroe=$(input).val().split(".")
    const long= numeroe[0].length;
    var newnum="";
    cont=0;
    for(var i=(long-1);i>=0;i--){
          if(cont%3==0 && cont!=0){
            newnum=numeroe[0].charAt(i)+","+newnum;
            
            cont+=1;
          }else{
            
            newnum=numeroe[0].charAt(i)+newnum;
            cont+=1;
          }
    }
    $(input).val(newnum+"."+numeroe[1]);
    }
    
  }