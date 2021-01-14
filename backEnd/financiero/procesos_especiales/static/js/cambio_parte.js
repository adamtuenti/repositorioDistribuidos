var valorTevento=0;
var codTevento=0;

$('.select3').select2({  
    tags: true,
    dropdownParent: $("#CambiarParticipante").parent(),
    minimumInputLength: 0,
    width: '100%',
    language: {
      noResults: function () {
        return "No hay resultados";
      },
      searching: function () {
  
        return "Buscando...";
      }
      ,
      inputTooShort: function (e) {
        var t = e.minimum - e.input.length;
        return "Ingresa " + t + " caractéres para buscar";
      }
    }

   
  });



function load_eventos() {
    console.log("yep")
    var url = $('#form-part').attr("data-eventos-url");
      $.ajax({
        url: url,
        data: {
          'tipo': "Part",
        },
        success: function (data) {
          console.log(data)
          $("#id_codigo_evento").html(data.eventos);
        }
      });
      
  };

function datos_eventos(){
    var url = $('#form-part').attr("data-eventosInd-url");
      $.ajax({
        url: url,
        data: {
            'codigo': $("#id_codigo_evento").val(),
          },
        success: function (data) {
          var evento=data.evento;
          $("#id_nombre_evento").val(evento.nombre);
          $("#id_fecha_inicio").val(evento.fecha_inicio);
          $("#id_fecha_fin").val(evento.fecha_fin);
          $("#id_lugar_evento").val(evento.lugar);

          // $("#codtO").html($("#id_codigo_evento").val());
          // $("#valtO").html(data.valor);
          // $("#codtD").html($("#id_codigo_evento").val());
          // $("#valtD").html(data.valor);
          valorTevento=transformN(data.valor);
          codTevento=$("#id_codigo_evento").val();
        }
      });
}
  
function cargar_participantes(){
  var url = $('#form-part').attr("data-participantesEvento-url");
  $.ajax({
    url: url,
    data: {
      'codigo': $("#id_codigo_evento").val(),
    },
    success: function (data) {
      $("#cedulaO").html(data.ruc_ci);
      $("#nombreO").html(data.razon_nombre);

      $("#cedtO").html("");
      $("#nomtO").html("");
      $("#codtO").html("");
      $("#valtO").html("");
      $($($("#valtO").parent()).children()[4]).html("");

      var url2= $('#form-part').attr("data-personarNaturalesNoenEvento-url");
      console.log(url2)
      $.ajax({
        url: url2,
        data: {
          'codigo': $("#id_codigo_evento").val(),
        },
        success: function (data) {
          console.log(data);
          $("#cedulaD").html(data.ruc_ci);
          $("#nombreD").html(data.razon_nombre);

          $("#cedtD").html("");
          $("#nomtD").html("");
          $("#codtD").html("");
          $("#valtD").html("");
          $($($("#valtD").parent()).children()[4]).html("");
        }
      });
    }
  });
}



function autocomplete(from, to) {
  if (from.val() != "") {
    $('#' + to).val($('#' + to + " option[name='" + from.val() + "']").val());
    $('#select2-' + to + '-container').text($('#' + to).val());
  }
  else {
    $('#' + to).val("");
    $('#select2-' + to + '-container').text("---------");
  }
}

  //Para los eventos
  load_eventos();
  

//   $(document).on('change', '#id_codigo_evento', function () {

//     if($("#id_codigo_evento").val()==""){
//       datos_eventos();
//       cargar_participantes();
//       $("#id_nombre_evento").val("");
//       $("#id_fecha_inicio").val("");
//       $("#id_fecha_fin").val("");
//       $("#id_lugar_evento").val("");

//       $("#cedulaO").prop("disabled",true);
//       $("#nombreO").prop("disabled",true);
//       $("#cedulaD").prop("disabled",true);
//       $("#nombreD").prop("disabled",true);
//     }else{
//       datos_eventos();
//       cargar_participantes();

//       $("#cedulaO").prop("disabled",false);
//       $("#nombreO").prop("disabled",false);
//       $("#cedulaD").prop("disabled",false);
//       $("#nombreD").prop("disabled",false);
//     }
//   });

//   $(document).on('change', '#cedulaO', function () {
//     autocomplete($(this), 'nombreO');
//     if($("#cedtO").html()=="" && $("#cedulaO").val()!=""){
//       $("#cedtO").html($("#cedulaO").val());
//       $("#nomtO").html($("#nombreO").val());
      
//       $("#codtO").html(codTevento);
//       $("#valtO").html(valorTevento);

//     var a=$("<a>");
//     a.attr("class","btn btn-danger btn-sm eliminarPart");
//     a.attr("href","#");
//     var i=$("<i>");
//     i.attr("class","fas fa-trash");
//     a.append(i);
//     $($($("#valtO").parent()).children()[4]).append(a);
//     }
    

//  });
 
//  $(document).on('change', '#nombreO', function () {
//   autocomplete($(this), 'cedulaO');
//   if($("#cedtO").html()=="" && $("#cedulaO").val()!=""){
//     $("#cedtO").html($("#cedulaO").val());
//     $("#nomtO").html($("#nombreO").val());
    
//     $("#codtO").html(codTevento);
//     $("#valtO").html(valorTevento);

//     var a=$("<a>");
//     a.attr("class","btn btn-danger btn-sm eliminarPart");
//     a.attr("href","#");
//     var i=$("<i>");
//     i.attr("class","fas fa-trash");
//     a.append(i);
//     $($($("#valtO").parent()).children()[4]).append(a);

//   }
// });


// $(document).on('change', '#cedulaD', function () {
//   autocomplete($(this), 'nombreD');
//   console.log($("#cedtD").html());
//   if($("#cedtD").html()=="" && $("#cedulaD").val()!=""){
//     $("#cedtD").html($("#cedulaD").val());
//     $("#nomtD").html($("#nombreD").val());
    
//     $("#codtD").html(codTevento);
//     $("#valtD").html(valorTevento);

//     var a=$("<a>");
//     a.attr("class","btn btn-danger btn-sm eliminarPart");
//     a.attr("href","#");
//     var i=$("<i>");
//     i.attr("class","fas fa-trash");
//     a.append(i);
//     $($($("#valtD").parent()).children()[4]).append(a);
//   }
  
// });

// $(document).on('change', '#nombreD', function () {
// autocomplete($(this), 'cedulaD');
// if($("#cedtD").html()=="" && $("#cedulaD").val()!=""){
//   $("#cedtD").html($("#cedulaD").val());
//   $("#nomtD").html($("#nombreD").val());
  
//   $("#codtD").html(codTevento);
//   $("#valtD").html(valorTevento);

//   var a=$("<a>");
//   a.attr("class","btn btn-danger btn-sm eliminarPart");
//   a.attr("href","#");
//   var i=$("<i>");
//   i.attr("class","fas fa-trash");
//   a.append(i);
//   $($($("#valtD").parent()).children()[4]).append(a);
// }
  
// });



// $(document).on('click', '#hack', function () {
  
//   $("#id_participante_origen_cedula").val($("#cedtO").html());
//     $("#id_participante_origen_nombre").val($("#nomtO").html());
//     $("#id_participante_destino_cedula").val($("#cedtD").html());
//     $("#id_participante_destino_nombre").val($("#nomtD").html());
//   });

// $(document).on('click', '.eliminarPart', function () {
  
//     var row=$(this).parent().parent();
//     $(row).children().each(function(){
//        $(this).html("");
//       //  if($(this).attr("id")=="cedtD"){
//       //     $("#cedulaD").val("");
//       //  }else if(($(this).attr("id")=="cedtO")){
//       //     $("#cedulaO").val("");
//       //  }
//     });
// });

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