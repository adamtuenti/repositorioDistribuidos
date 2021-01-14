$(".select3").select2({ 
    dropdownParent: $("#seguimientoInteresado").parent(),
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

function load_evento() {
    
    var url = $('#form-seguimiento-interesado').attr("datos-eventos-url");
      $.ajax({
        url: url,
        success: function (data) {
          $("#id_cod_evento").html(data.cod);
          $("#id_nombre_evento").html(data.nom);
  
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

  $(document).on('change', '#id_cod_evento', function () {
    autocomplete($(this), 'id_nombre_evento');
    
  });

  $(document).on('change', '#id_nombre_evento', function () {
    autocomplete($(this), 'id_cod_evento');
    
  });

  load_evento();