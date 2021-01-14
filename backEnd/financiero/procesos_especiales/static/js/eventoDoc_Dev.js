$(document).on('click', '.checkB', function () {
    
    if($(this).prop("checked") && $("#id_categoria").val()=="Dev"){
        var url = $("#form-pe").attr("data-verAs-url");
        var tdC=$(this).parent().parent().children()[0];
        var tdN=$(this).parent().parent().children()[1];
        $.ajax({
            url: url,
            data: {
              'codigo':$("#codigoEvento").val(),
              'cedula': $(tdC).html(),
              'nombre': $(tdN).html(),
            },
            success: function (data) {
              console.log(data.bandera);
              if (data.bandera){
                alert("El participante "+data.nombre+" tuvo asistencias menores al 20%")
              }else if(data.bandera2){
                alert("El participante "+data.nombre+" tuvo asistencias mayores al 20%")
              }
            }
          });
    }

    if($(this).prop("checked") && $("#id_categoria").val()=="Part"){

         $(".checkB").each(function(){
                  if(!$(this).prop("checked")){
                      $(this).hide();
                  }
         });

    }else if(!$(this).prop("checked") && $("#id_categoria").val()=="Part"){
      $(".checkB").each(function(){
        
            $(this).show();
        
      });
    }

    if($(this).prop("checked") && $("#id_categoria").val()=="Event" && $("#id_tipo_nota").val()=="Débito"){

      $(".checkB").each(function(){
          if(!$(this).prop("checked")){
                $(this).hide();
          }
      });

    }else if(!$(this).prop("checked") && $("#id_categoria").val()=="Event" && $("#id_tipo_nota").val()=="Débito"){

      $(".checkB").each(function(){
        
        $(this).show();
    
        });

    }

  });