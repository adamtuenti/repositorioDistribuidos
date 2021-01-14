var lista=[]
contI=0;
$(document).on('click', '#agregar', function () {
    $("#participantesTabla tbody tr").each(function(){
        var checked=$(this).find("input");
        if($(checked).prop("checked") == true && $(checked).attr('disabled')!="disabled"){
            var cedula=$($(this).children()[0]).html();
            if(!(lista.includes(cedula))){
                lista.push(cedula)
                console.log($($(this).children()[0]).html())
            }
        }
    });
    
    if(contI==0){
        console.log(lista)
        lista=JSON.stringify({ 'lista': lista, 'codigo': $("#codigoEasy").html()});
        console.log(lista)
        $.ajax({
            url: $("#form-pe").attr("data-partList-url"),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            data: {
              'lista': lista,
            },
            success: function (data) {
              var participantes=data.participantes;
              console.log(participantes)
              for(var i=0;i<participantes.length;i++){
                console.log(participantes[i]);
                var total = $('#id_procesoparticipante_set-TOTAL_FORMS').val();
                $("#id_procesoparticipante_set-"+(total-1)+"-participante").val(participantes[i].participante_id);
                $("#id_procesoparticipante_set-"+(total-1)+"-nombre_evento").val(participantes[i].nombre_evento);
                $("#id_procesoparticipante_set-"+(total-1)+"-cod_evento").val(participantes[i].cod_evento);
                $("#id_procesoparticipante_set-"+(total-1)+"-valor_evento").val(participantes[i].valor_evento);
                $("#id_procesoparticipante_set-"+(total-1)+"-descuento").val($("#id_descuentoC").val());
                var desc= parseInt($("#id_descuentoC").val());
                var valor=participantes[i].valor_evento;
                var vt= valor-((valor*desc)/100);
                console.log(vt)
                $("#id_procesoparticipante_set-"+(total-1)+"-valor").val(vt);
                $("#id_procesoparticipante_set-"+(total-1)+"-orden").val(participantes[i].orden_id);
                $("#MEGAHACK").trigger("click");

              }
              $("#MEGAHACK").trigger("actualizar");
            }
          });
        contI=1
    }


  });




  
tabla={}
console.log("camibo memingasd")
$("#tbodyPart tr").each(function(){
    var children=$(this).children();
    var codigo= $(children[2]).html();

    var participante=$(children[0]).html();
    var cedula=participante.split(" ")[0];
    if(tabla[cedula]!=undefined){
        tabla[cedula].push(codigo);
    }else{
        lista=[]
        lista.push(codigo);
        tabla[cedula]=lista;
    }
});
  


$("#participantesTabla tr").each(function(){
  var children=$(this).children();
  var codigo= $(children[2]).html();

  var cedula=$(children[0]).html();

  if(tabla[cedula]!=undefined){
    if(tabla[cedula].includes(codigo)){
      var check=$(children[4]).find("input");
      $(check).prop("checked",true);
      $(check).attr('disabled', 'disabled');
      
    }
  }
});

$("#BodyNumberPart tr").each(function(){
  var children=$(this).children();
  
  $(children[3]).html(transformN($(children[3]).html()));
});


function transformN(numero){
  var num=""+parseFloat(numero).toFixed(2);
  var numeroe=num.split(".")
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
  return "$"+newnum+"."+numeroe[1];
  
}