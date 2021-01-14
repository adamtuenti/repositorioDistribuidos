//seccion de signo de dolar
var monto=$("#div_id_monto_propuesta");
var inp=$("#div_id_monto_propuesta input");
var hijos=monto.children();
const dnuevo=hijos[1];
dnuevo.remove();
const dollar=$("<div>");
dollar.attr("class","input-icon")
const icono=$("<i>");
icono.text("$");
dollar.append(inp);
dollar.append(icono);
monto.append(dollar);


var utilidad=$("#div_id_utilidad_esperada");
var inpu=$("#div_id_utilidad_esperada input");
var hijosu=utilidad.children();
const dnuevou=hijosu[1];
dnuevou.remove();
const dollaru=$("<div>");
dollaru.attr("class","input-icon")
const iconou=$("<i>");
iconou.text("$");
dollaru.append(inpu);
dollaru.append(iconou);
utilidad.append(dollaru);

//Codigo para controlar la version
const ver=parseInt($("#id_version").val());
if($("#ac").val()=="True"){
  $(document).on('change', "#id_version", function (e) {
    const veract=parseInt($("#id_version").val());
    if(veract>(ver+1)){
      $(this).val(ver+1)
    }else if(veract<ver){
      $(this).val(ver)
    }
  });
}else{
  $("#id_version").prop('disabled', true);
}




if($("#id_monto_propuesta").val()!=""){
  transform($("#id_monto_propuesta"));
}

$("#id_monto_propuesta").focusout(function() {
  transform($(this));
})
$("#id_monto_propuesta").focus(function() {
const val=$(this).val();
$(this).attr("type","number");
$(this).val(parseFloat(val.replace(/,/g,"")));
$(this).val(parseFloat($(this).val()).toFixed(2));
})

if($("#id_utilidad_esperada").val()!=""){
  transform($("#id_utilidad_esperada"));
}

$("#id_utilidad_esperada").focusout(function() {
  transform($(this));
})
$("#id_utilidad_esperada").focus(function() {
const val=$(this).val();
$(this).attr("type","number");
$(this).val(parseFloat(val.replace(/,/g,"")));
$(this).val(parseFloat($(this).val()).toFixed(2));
})

function transform(input){
  if($(input).val()!=""){
    $(input).val(parseFloat($(input).val()).toFixed(2));
  $(input).attr("type","text");
  console.log($(input).val())
  var numeroe=$(input).val().split(".")
  const long= numeroe[0].length;
  console.log(long)
  var newnum="";
  cont=0;
  for(var i=(long-1);i>=0;i--){
        if(cont%3==0 && cont!=0){
          newnum=numeroe[0].charAt(i)+","+newnum;
          console.log("coma");
          console.log(i);
          console.log(numeroe[0].charAt(i));
          cont+=1;
        }else{
          console.log("no coma");
          console.log(i);
          console.log(numeroe[0].charAt(i));
          newnum=numeroe[0].charAt(i)+newnum;
          cont+=1;
        }
  }
  console.log(newnum+"."+numeroe[1]);
  $(input).val(newnum+"."+numeroe[1]);
  }
  
}