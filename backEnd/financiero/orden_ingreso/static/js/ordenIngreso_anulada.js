function Ocultar(){
    var estado = $('input#id_estado');
    var boton_anulado = $('a#anular_orden_ingreso')
    var boton_guardar = $('button#guardar_orden_ingreso');
    var numero_tramite = $('input#id_n_tramite');
    var fecha_tramite = $('input#id_fecha_tramite');
    var fecha_pago = $('input#id_fechaPago');
    var anexo = $('input#id_anexo');

    var campos = [numero_tramite,fecha_tramite,fecha_pago];

    if ($(estado).val()=="ANLD"){
       campos.forEach(function(value,index){
          $(campos[index]).attr('readonly',"True");
       });

       //Para el anexo no funciona el readonly, es necesario usar disabled
       $(anexo).attr('disabled',"");
       $(boton_anulado).remove();
       $(boton_guardar).remove();
       var anexos=$(".ingresof");
       $(anexos[anexos.length-1]).parent().parent().parent().parent().remove();
       $(".ingresof").each(function(){
         $(this).prop("disabled",true)
      });
      $("td input[type=checkbox]").each(function() {
         $(this).parent().remove();
         $(this).remove();
       });
       $("td a + input").each(function() {
         $(this).remove();
     });
 
     $("td a + label").each(function() {
         $(this).remove();
     });
 
     $("td input[type=checkbox]").each(function() {
         $(this).parent().remove();
         $(this).remove();
     });
 
     $("#tablefile tr").each(function(){
         var h=$(this).children();
         var parent=$(h[0]).find("input[type=file]").parent();
         console.log($(parent).children());
         var anex=undefined;
         $(parent).children().each(function(){
             console.log($(this));
             if($(this).prop("tagName")=="BR" ||$(this).prop("tagName")=="INPUT"){
                 $(this).remove();
             }else if($(this).prop("tagName")=="A"){
                 anex=$(this);
             }
         })
         $(parent).html("");
         $(parent).html("Actual:");
         $(parent).append(anex);
         
     });
    }
    
    
  }
  $(document).ready(function () {
      Ocultar();
  });