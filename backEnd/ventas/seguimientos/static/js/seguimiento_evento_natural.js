$('.select3').select2({
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


  function load_evento_o() {
    
    var url = $('#form-segEvent').attr("data-eventO-url");
      $.ajax({
        url: url,
        success: function (data) {
          $("#id_codigo_eventoO").html(data.cod);
          $("#id_nombre_eventoO").html(data.nom);
        }
      });
      
  };

  function load_evento_d() {
    
    var url = $('#form-segEvent').attr("data-eventD-url");
      $.ajax({
        url: url,
        data: {
            'cod_evento': $("#id_codigo_eventoO").val(),
          },
        success: function (data) {
          $("#id_codigo_eventoD").html(data.cod);
          $("#id_nombre_eventoD").html(data.nom);
        }
      });
      
  };

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


  $(document).on('change', '#id_codigo_eventoO', function () {
    autocomplete($(this), 'id_nombre_eventoO');
    load_evento_d()
  });

  $(document).on('change', '#id_nombre_eventoO', function () {
    autocomplete($(this), 'id_codigo_eventoO');
    load_evento_d()
  });

  $(document).on('change', '#id_codigo_eventoD', function () {
    autocomplete($(this), 'id_nombre_eventoD');
    
  });

  $(document).on('change', '#id_nombre_eventoD', function () {
    autocomplete($(this), 'id_codigo_eventoD');
    
  });


  load_evento_o();

  //para haver bold los labels del evento destino
  var labeln=$("#div_id_nombre_eventoD").find("label");
  $(labeln).attr("class", $(labeln).attr("class")+" font-weight-bold");
  var labelc=$("#div_id_codigo_eventoD").find("label");
  $(labelc).attr("class", $(labelc).attr("class")+" font-weight-bold");