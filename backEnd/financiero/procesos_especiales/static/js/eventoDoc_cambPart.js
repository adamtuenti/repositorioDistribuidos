$(document).on('change', '#id_codigo_evento', function () {

        if($("#id_codigo_evento").val()==""){
          // datos_eventos();
          // cargar_participantes();
          console.log("entro a cuando no tiene valor");
          $("#id_nombre_evento").val("");
          $("#id_fecha_inicio").val("");
          $("#id_fecha_fin").val("");
          $("#id_lugar_evento").val("");
    
          $("#cedulaO").prop("disabled",true);
          $("#nombreO").prop("disabled",true);
          $("#cedulaD").prop("disabled",true);
          $("#nombreD").prop("disabled",true);


          $("#cedulaO").val("").trigger("change");
          $("#nombreO").val("").trigger("change");
          $("#cedulaD").val("").trigger("change");
          $("#nombreD").val("").trigger("change");

          $("#participante-origen").find("td").each(function(){
            console.log($(this));
            $(this).html("");
          });

          $("#participante-destino").find("td").each(function(){
            console.log($(this));
            $(this).html("");
          });

          

        }else{
          console.log("entro a cuando tiene valor")
          datos_eventos();
          cargar_participantes();
    
          $("#cedulaO").prop("disabled",false);
          $("#nombreO").prop("disabled",false);
          $("#cedulaD").prop("disabled",false);
          $("#nombreD").prop("disabled",false);
        }
      });
    
      // $(document).on('click', '#div_id_codigo_evento span.select2-selection', function () {
      //       load_eventos();
           
      //       console.log("se clickeo");
      // });


      $(document).on('change', '#cedulaO', function () {
        autocomplete($(this), 'nombreO');
        if($("#cedtO").html()=="" && $("#cedulaO").val()!=""){
          $("#cedtO").html($("#cedulaO").val());
          $("#nomtO").html($("#nombreO").val());
          
          $("#codtO").html(codTevento);
          $("#valtO").html(valorTevento);
    
        var a=$("<a>");
        a.attr("class","btn btn-danger btn-sm eliminarPart");
        a.attr("href","#");
        var i=$("<i>");
        i.attr("class","fas fa-trash");
        a.append(i);
        $($($("#valtO").parent()).children()[4]).append(a);
        AlarmaAsistencia();
        }
        
    
     });
     
     $(document).on('change', '#nombreO', function () {
      autocomplete($(this), 'cedulaO');
      if($("#cedtO").html()=="" && $("#cedulaO").val()!=""){
        $("#cedtO").html($("#cedulaO").val());
        $("#nomtO").html($("#nombreO").val());
        
        $("#codtO").html(codTevento);
        $("#valtO").html(valorTevento);
    
        var a=$("<a>");
        a.attr("class","btn btn-danger btn-sm eliminarPart");
        a.attr("href","#");
        var i=$("<i>");
        i.attr("class","fas fa-trash");
        a.append(i);
        $($($("#valtO").parent()).children()[4]).append(a);
        AlarmaAsistencia();
      }
    });
    
    
    $(document).on('change', '#cedulaD', function () {
      autocomplete($(this), 'nombreD');
      console.log($("#cedtD").html());
      if($("#cedtD").html()=="" && $("#cedulaD").val()!=""){
        $("#cedtD").html($("#cedulaD").val());
        $("#nomtD").html($("#nombreD").val());
        
        $("#codtD").html(codTevento);
        $("#valtD").html(valorTevento);
    
        var a=$("<a>");
        a.attr("class","btn btn-danger btn-sm eliminarPart");
        a.attr("href","#");
        var i=$("<i>");
        i.attr("class","fas fa-trash");
        a.append(i);
        $($($("#valtD").parent()).children()[4]).append(a);
      }
      
    });
    
    $(document).on('change', '#nombreD', function () {
    autocomplete($(this), 'cedulaD');
    if($("#cedtD").html()=="" && $("#cedulaD").val()!=""){
      $("#cedtD").html($("#cedulaD").val());
      $("#nomtD").html($("#nombreD").val());
      
      $("#codtD").html(codTevento);
      $("#valtD").html(valorTevento);
    
      var a=$("<a>");
      a.attr("class","btn btn-danger btn-sm eliminarPart");
      a.attr("href","#");
      var i=$("<i>");
      i.attr("class","fas fa-trash");
      a.append(i);
      $($($("#valtD").parent()).children()[4]).append(a);
    }
      
    });
    
    
    
    $(document).on('click', '#hack', function () {
      
      $("#id_participante_origen_cedula").val($("#cedtO").html());
        $("#id_participante_origen_nombre").val($("#nomtO").html());
        $("#id_participante_destino_cedula").val($("#cedtD").html());
        $("#id_participante_destino_nombre").val($("#nomtD").html());
      });
    
    $(document).on('click', '.eliminarPart', function () {
      
        var row=$(this).parent().parent();
        $(row).children().each(function(){
           $(this).html("");
          //  if($(this).attr("id")=="cedtD"){
          //     $("#cedulaD").val("");
          //  }else if(($(this).attr("id")=="cedtO")){
          //     $("#cedulaO").val("");
          //  }
        });
    });


//Alarma del 20% de asistencias
function AlarmaAsistencia(){

        var url = $("#form-part").attr("data-verAs-url");
        var tdC=$("#id_codigo_evento").val();
        var tdN=$("#nombreO").val();
        var tdCed=$("#cedulaO").val();
        $.ajax({
            url: url,
            data: {
              'codigo': tdC,
              'cedula': tdCed,
              'nombre': tdN,
            },
            success: function (data) {
              console.log(data.bandera2);
              if(data.bandera2){
                alert("El participante "+data.nombre+" tuvo asistencias mayores al 20%")
              }
            }
          });


}