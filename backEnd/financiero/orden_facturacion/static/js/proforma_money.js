//seccion de signo de dolar
var monto=$("#div_id_montoDesc");
var inp=$("#div_id_montoDesc input");
var hijos=monto.children();
var d=hijos[1];
d.remove();
var dollar=$("<div>");
dollar.attr("class","input-icon")
var icono=$("<i>");
icono.text("$");
dollar.append(inp);
dollar.append(icono);
monto.append(dollar);

//seccion de signo de dolar
var montou=$("#div_id_montoProforma");
var inpu=$("#div_id_montoProforma input");
var hijosu=montou.children();
var du=hijosu[1];
du.remove();
var dollaru=$("<div>");
dollaru.attr("class","input-icon")
var iconou=$("<i>");
iconou.text("$");
dollaru.append(inpu);
dollaru.append(iconou);
montou.append(dollaru);

//seccion de signo de dolar
var montoa=$("#div_id_montoAceptado");
var inpa=$("#div_id_montoAceptado input");
var hijosa=montoa.children();
var da=hijosa[1];
da.remove();
var dollara=$("<div>");
dollara.attr("class","input-icon")
var iconoa=$("<i>");
iconoa.text("$");
dollara.append(inpa);
dollara.append(iconoa);
montoa.append(dollara);

//seccion de signo de dolar
var montoe=$("#div_id_montoPorEjecutarse");
var inpe=$("#div_id_montoPorEjecutarse input");
var hijose=montoe.children();
var de=hijose[1];
de.remove();
var dollare=$("<div>");
dollare.attr("class","input-icon")
var iconoe=$("<i>");
iconoe.text("$");
dollare.append(inpe);
dollare.append(iconoe);
montoe.append(dollare);

//seccion de signo de dolar
var montoeo=$("#div_id_montoEjecutado");
var inpeo=$("#div_id_montoEjecutado input");
var hijoseo=montoeo.children();
var deo=hijoseo[1];
deo.remove();
var dollareo=$("<div>");
dollareo.attr("class","input-icon")
var iconoeo=$("<i>");
iconoeo.text("$");
dollareo.append(inpeo);
dollareo.append(iconoeo);
montoeo.append(dollareo);

//para poder controlar las versiones
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


if($("#id_montoProforma").val()!=""){
  transform($("#id_montoProforma"));
}

$("#id_montoProforma").focusout(function() {
    transform($(this));
})
$("#id_montoProforma").focus(function() {
  const val=$(this).val();
  $(this).attr("type","number");
  $(this).val(parseFloat(val.replace(/,/g,"")));
  $(this).val(parseFloat($(this).val()).toFixed(2));
})

if($("#id_montoDesc").val()!=""){
  transform($("#id_montoDesc"));
}

$("#id_montoDesc").focusout(function() {
  transform($(this));
})
$("#id_montoDesc").focus(function() {
const val=$(this).val();
$(this).attr("type","number");
$(this).val(parseFloat(val.replace(/,/g,"")));
$(this).val(parseFloat($(this).val()).toFixed(2));
})

if($("#id_montoAceptado").val()!=""){
  transform($("#id_montoAceptado"));
}

$("#id_montoAceptado").focusout(function() {
  transform($(this));
})
$("#id_montoAceptado").focus(function() {
const val=$(this).val();
$(this).attr("type","number");
$(this).val(parseFloat(val.replace(/,/g,"")));
$(this).val(parseFloat($(this).val()).toFixed(2));
})

if($("#id_montoEjecutado").val()!=""){
  transform($("#id_montoEjecutado"));
}

$("#id_montoEjecutado").focusout(function() {
  transform($(this));
})
$("#id_montoEjecutado").focus(function() {
const val=$(this).val();
$(this).attr("type","number");
$(this).val(parseFloat(val.replace(/,/g,"")));
$(this).val(parseFloat($(this).val()).toFixed(2));
})

if($("#id_montoPorEjecutarse").val()!=""){
  transform($("#id_montoPorEjecutarse"));
}

$("#id_montoPorEjecutarse").focusout(function() {
  transform($(this));
})
$("#id_montoPorEjecutarse").focus(function() {
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