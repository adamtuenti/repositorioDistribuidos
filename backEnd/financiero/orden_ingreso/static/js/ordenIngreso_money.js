let numero_final ;
//Cambiar el signo de dolar
var valor=$("#div_id_valor");
var inp=$("#div_id_valor input");
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


//Funcion para establecer Formato de Dinero
function formatNumber(num) {
  return num.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

function Transform(input){
  var numero = $(input).val();
  $(input).attr("type","text");
  var numero_transformado = "";
  numero_final = numero;
  if(numero != "" ){
    numero_transformado = formatNumber(numero);
  }
  if(numero != "" && !numero.includes(".")){
    numero_transformado+=".00";
  }
  $(input).val(numero_transformado);
}


$(document).ready(function () {
  var entrada = $("input#id_valor");
  var estado = $('input#id_estado');
  $(entrada).focus(function (e) { 
    if ($(estado).val()!="ANLD"){
      $(entrada).attr("type","number");
      $(entrada).val(numero_final);
    }
  });

  $(entrada).focusout(function (e) { 
    
    Transform(entrada);
    
  });

  $("button").click(function (e) {
    $(entrada).attr("type","number");
    if(numero_final == undefined ){
      numero_final = $(entrada).val();
      $(entrada).val(numero_final);  
    }
    else{
      $(entrada).val(numero_final);  
    }
  });
});
// function transform(input){
//     if($(input).val()!=""){
//       $(input).val(parseFloat($(input).val()).toFixed(2));
//     $(input).attr("type","text");
//     console.log($(input).val())
//     var numeroe=$(input).val().split(".")
//     const long= numeroe[0].length;
//     console.log(long)
//     var newnum="";
//     cont=0;
//     for(var i=(long-1);i>=0;i--){
//           if(cont%3==0 && cont!=0){
//             newnum=numeroe[0].charAt(i)+","+newnum;
//             console.log("coma");
//             console.log(i);
//             console.log(numeroe[0].charAt(i));
//             cont+=1;
//           }else{
//             console.log("no coma");
//             console.log(i);
//             console.log(numeroe[0].charAt(i));
//             newnum=numeroe[0].charAt(i)+newnum;
//             cont+=1;
//           }
//     }
//     console.log(newnum+"."+numeroe[1]);
//     $(input).val(newnum+"."+numeroe[1]);
//     }
    
//   }



//   //Una vez listo el documento
//   $(document).ready(function () {
//     var input = $("#id_valor");

//     if($(input).val()!="" || $(input).val()!=NaN ){
//         transform($(input));
//       }
      
//       $(input).focusout(function() {
//         transform($(this));
//       })
//       $(input).focus(function() {
//       const val=$(this).val();
//       $(this).attr("type","number");
//       $(this).val(parseFloat(val.replace(/,/g,"")));
//       $(this).val(parseFloat($(this).val()).toFixed(2));
//       })
//   });