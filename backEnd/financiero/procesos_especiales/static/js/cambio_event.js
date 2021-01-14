$('.select4').select2({
  tags: true,
  dropdownParent: $("#CambiarEvento").parent(),
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

function load_participantes() {
    
  var url = $('#form-event').attr("data-participantes-url");
    $.ajax({
      url: url,
      success: function (data) {
        $("#id_participante_cedula").html(data.ruc_ci);
        $("#id_participante_nombre").html(data.razon_nombre);
      }
    });
    
};
console.log("12")
function load_participante_evento() {
    
  var url = $('#form-event').attr("data-partEvento-url");
    $.ajax({
      url: url,
      data: {
        'cedula': $("#id_participante_cedula").val(),
      },
      success: function (data) {
        $("#codigoO").html(data.cod);
        $("#nombreEO").html(data.nom);

        $("#codtEO").html("");
        $("#nomtEO").html("");
        $("#fitEO").html("");
        $("#fftEO").html("");
        $("#evtEO").html("");
        $($($("#evtEO").parent()).children()[5]).html("");

      }
    });
    
};

function load_participanteNo_evento() {
    
  var url = $('#form-event').attr("data-nopartEvento-url");
    $.ajax({
      url: url,
      data: {
        'cedula': $("#id_participante_cedula").val(),
      },
      success: function (data) {
        $("#codigoD").html(data.cod);
        $("#nombreED").html(data.nom);

        $("#codtED").html("");
        $("#nomtED").html("");
        $("#fitED").html("");
        $("#fftED").html("");
        $("#evtED").html("");
        $($($("#evtED").parent()).children()[5]).html("");
      }
    });
    
};

function datos_eventos2(codigo, tipo){
  var url = $('#form-event').attr("data-eventosInd-url");
  
    $.ajax({
      url: url,
      data: {
          'codigo': codigo,
        },
      success: function (data) {
        var evento=data.evento;
        console.log(data)
        console.log("jeje si sale")
        if(tipo=="DESTINO"){
          console.log("entro destino");
          CrearFila(data.evento,data.valor);

        }else{
          console.log("entro origen");
          $("#codtEO").html(evento.codigo_evento);
          $("#nomtEO").html(evento.nombre);
          $("#fitEO").html(evento.fecha_inicio);
          $("#fftEO").html(evento.fecha_fin);
          $("#evtEO").html(transformN(data.valor));

          var a=$("<a>");
          a.attr("class","btn btn-danger btn-sm eliminarEvent");
          a.attr("href","#");
          var i=$("<i>");
          i.attr("class","fas fa-trash");
          a.append(i);
          $($($("#evtEO").parent()).children()[5]).append(a);

        }
      }
    });
}
console.log("cambio")
function CrearFila(evento,valor){
      var num=$("#id_form-TOTAL_FORMS").val();
      console.log(num)
      $("#id_form-"+(num-1)+"-evento_destino_codigo").val(evento.codigo_evento);
      $("#id_form-"+(num-1)+"-evento_destino_nombre").val(evento.nombre);
      $("#id_form-"+(num-1)+"-evento_destino_valor").val(valor);

      var row=$("<tr>");
      row.attr("class","text-center");
      var codigo=$("<td>").html(evento.codigo_evento);
      var nombre=$("<td>").html(evento.nombre);
      var fechai=$("<td>").html(evento.fecha_inicio);
      var fechaf=$("<td>").html(evento.fecha_fin);
      var valorE=$("<td>").html(transformN(valor));
      var acciones=$("<td>");

      var a=$("<a>");
      a.attr("class","btn btn-danger btn-sm eliminarEventoDinamico");
      a.attr("href","#");
      var i=$("<i>");
      i.attr("class","fas fa-trash");
      a.append(i);
      acciones.append(a);

      row.append(codigo);
      row.append(nombre);
      row.append(fechai);
      row.append(fechaf);
      row.append(valorE);
      row.append(acciones);

      $("#EventoDestinoTablaBody").append(row);
      cloneMore('.latruept:last', 'form');
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



// $(document).on('change', '#id_participante_cedula', function () {
//   autocomplete($(this), 'id_participante_nombre');
//   if($("#id_participante_cedula").val()==""){
//     $("#codigoO").prop("disabled",true);
//     $("#nombreEO").prop("disabled",true);
//     $("#codigoD").prop("disabled",true);
//     $("#nombreED").prop("disabled",true);
//   }else{
//     load_participante_evento();
//     load_participanteNo_evento();
//     $("#codigoO").prop("disabled",false);
//     $("#nombreEO").prop("disabled",false);
//     $("#codigoD").prop("disabled",false);
//     $("#nombreED").prop("disabled",false);
//   }
// });

// $(document).on('change', '#id_participante_nombre', function () {
//   autocomplete($(this), 'id_participante_cedula');
//   if($("#id_participante_cedula").val()==""){
//     $("#codigoO").prop("disabled",true);
//     $("#nombreEO").prop("disabled",true);
//     $("#codigoD").prop("disabled",true);
//     $("#nombreED").prop("disabled",true);
    
//   }else{
//     load_participante_evento();
//     load_participanteNo_evento();
//     $("#codigoO").prop("disabled",false);
//     $("#nombreEO").prop("disabled",false);
//     $("#codigoD").prop("disabled",false);
//     $("#nombreED").prop("disabled",false);
//   }
// });

// $(document).on('change', '#codigoO', function () {
//   autocomplete($(this), 'nombreEO');
//   if($("#codtEO").html()=="" && $("#codigoO").val()!=""){
//     datos_eventos2($("#codigoO").val(), "ORIGEN");
//   }
  
// });

// $(document).on('change', '#nombreEO', function () {
//   autocomplete($(this), 'codigoO');
//   if($("#codtEO").html()=="" && $("#codigoO").val()!=""){
//     datos_eventos2($("#codigoO").val(), "ORIGEN");
//   }
  
// });

// $(document).on('change', '#codigoD', function () {
//   autocomplete($(this), 'nombreED');
//   console.log(verificarExistenciaEvento($("#codigoD").val()))
//   if($("#codigoD").val()!="" && verificarExistenciaEvento($("#codigoD").val())){
//     datos_eventos2($("#codigoD").val(), "DESTINO");
//   }
  
// });

// $(document).on('change', '#nombreED', function () {
//   autocomplete($(this), 'codigoD');
//   if($("#codigoD").val()!="" && verificarExistenciaEvento($("#codigoD").val())){
//     datos_eventos2($("#codigoD").val(), "DESTINO");
//   }
// });

// $(document).on('click', '#hack2', function () {
//     $("#id_evento_origen_codigo").val($("#codtEO").html());
//     $("#id_evento_origen_nombre").val($("#nomtEO").html());
//     $("#id_evento_origen_valor").val($("#evtEO").html());
//   });



// $(document).on('click', '.eliminarEvent', function () {
//   var row=$(this).parent().parent();
//   $(row).children().each(function(){
//      $(this).html("");
//   });
// });

// $(document).on('click', '.eliminarEventoDinamico', function () {
//   var row=$(this).parent().parent();
//   var children=row.children();
//   var cod=$(children[0]).html();
//   console.log(cod)
//   deleteForm('form', cod);
//   row.remove();
// });

load_participantes();

function verificarExistenciaEvento(codigo){
  var cont=0;
  var bandera=true;
    $(".latruept").each(function(){
        if($("#id_form-"+cont+"-evento_destino_codigo").val()==codigo){
              console.log("retorno false")
              bandera=false;
        }
        cont=cont+1;
    });

  return bandera;
}

function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp('(' + prefix + '-\\d+)');
  var replacement = prefix + '-' + ndx;
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}


function cloneMore(selector, prefix) {
  var newElement = $(selector).clone(true);
  var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
  newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
      var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
  });
  newElement.find('label').each(function() {
      var forValue = $(this).attr('for');
      if (forValue) {
        forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
        $(this).attr({'for': forValue});
      }
  });
  total++;
  $('#id_' + prefix + '-TOTAL_FORMS').val(total);
  $(selector).after(newElement);
  
  return false;
}

function deleteForm(prefix, codigo) {
  var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
  if (total > 1){
      
    cont=0;
    $(".latruept").each(function(){
        if($("#id_form-"+cont+"-evento_destino_codigo").val()==codigo){
              console.log("match")
              $(this).remove();
        }
        cont=cont+1;
    });

      var forms = $('.latruept');
      $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
      for (var i=0, formCount=forms.length; i<formCount; i++) {
          $(forms.get(i)).find(':input').each(function() {
              updateElementIndex(this, prefix, i);
          });
      }
  }
  return false;
}


   
deleteForm('form', $(this));


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