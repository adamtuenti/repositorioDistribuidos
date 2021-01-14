var bienes_cargados = {};
var opciones_selectores = {};

function formatoSelect(){
    $('.select4').select2({
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
    }
      
    
function load_bienes(id,bien,select_type) {

  $('#'+id).html(bienes_cargados[select_type]);
  //$('#'+id).val($('#id_bien').val()).trigger('change.select2');
  if(bien!=null){
    $("#"+id).val(bien);
    $("#"+id).trigger("change");
  }          
};

function load_data() {
  var url = $('#Calificacion_proveedorForm').attr("data-bien-url");
  var tipo = $("#id_tipo_bienes").val();
  if (tipo != "") {
      $("#div_cod_Inventariound").removeClass('d-none');
      $("#div_cod_bien").removeClass('d-none');
      $("#div_nombre").removeClass('d-none');
      $.ajax({
          url: url,
          data: {
              'tipo_Bien': tipo
          },
          success: function (data) {
              bienes_cargados["cod_Inventariound"] = data.cod_Inventariound;
              bienes_cargados["cod_bien"] = data.cod_bien;
              bienes_cargados["nombre"] = data.nombre;
              // $('#cod_In ventariound').val($('#id_bien').val()).trigger('change.select2');
              // $('#cod_bien').val($('#id_bien').val()).trigger('change.select2');
              // $('#nombre').val($('#id_bien').val()).trigger('change.select2');
          }
      });

  }
  else {
      $("#div_cod_Inventariound").addClass('d-none');
      $("#div_cod_bien").addClass('d-none');
      $("#div_nombre").addClass('d-none');
      $("#id_bien").val(null);
  }
};

$(document).on('change', '.selectBien', function () {
      var id=$(this).val();
      var idFP=$(this).attr("id");
      if(id!=""){
          var url = $('#Calificacion_proveedorForm').attr("data-bienInd-url");
          $.ajax({
              url: url,
              data:{
                  'id_bien':id,
              },
              success: function (data) {
                  // var idF=data.idF;
                  var fila=$("#"+idFP).parent().parent();
                  console.log(fila);
                  var hijos= fila.children();
                  $(hijos[3]).html(data.caracteristicas);
                  $(hijos[4]).html(data.marca);
                  $(hijos[5]).html(data.modelo);
                  $(hijos[6]).html(data.n_serie);
              }
          });
      }else{
          console.log("borrar")
          var fila=$(this).parent().parent();
          var hijos= fila.children();
          $(hijos[3]).html("")
          $(hijos[4]).html("")
          $(hijos[5]).html("")
          $(hijos[6]).html("")
          $($(hijos[7]).children()[0]).val(null)
          $($(hijos[8]).children()[0]).val(null)
          $($(hijos[9]).children()[0]).val(null)
          $($(hijos[10]).children()[0]).val(null)
          $($(hijos[11]).children()[0]).val(null)
          $($(hijos[12]).children()[0]).val(null)
          $($(hijos[13]).children()[0]).val(null)
      }
      fila=$(this).parent().parent();
      hijos= fila.children();
      autocomplete($(this), $($(hijos[0]).children()[0]).attr('id'));
      autocomplete($(this), $($(hijos[1]).children()[0]).attr('id'));
      autocomplete($(this), $($(hijos[2]).children()[0]).attr('id'));
});

$(document).on('click', '#add', function () {
    var hijos=$("#productoTableBody").children();
    var lastH=hijos[hijos.length-1];
    var sub=$($(lastH).children()[9]).html();
    if(sub!=''){
      crearFila(null);
      // cloneMoreM('.pt:last', 'productosuministro_set');
    }
    

  
});

function crearFila(bien){
        var fila=$("<tr>");
        fila.attr("class","text-center")
        var tdCI=$("<td>");
        var tdCE=$("<td>");
        var tdNB=$("<td>");
        var tdCA=$("<td>");
        var tdMA=$("<td>");
        var tdMO=$("<td>");
        var tdSE=$("<td>");
        var tdFI=$("<td>");
        var tdCO=$("<td>");
        var tdOB=$("<td>");
        var tdUR=$("<td>");
        var tdSede=$("<td>");
        var tdUB=$("<td>");
        var tdES=$("<td>");
        var tdA=$("<td>");

        // Selectores de bienes
        var sel1=$("<select>");
        sel1.attr("class","form-control select4 selectBien SP");
        var hijosid=$("#productoTableBody").children();
        if(hijosid.length==0){
          var id_codInv="SP-codInv-0";
          var id_codEspol="SP-codEspol-0";
          var id_nombre="SP-nombre-0";
          console.log("entro al if")
        }else{
          console.log("entro al else")
          var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
          var id_codInv="SP-codInv-"+(parseInt(nom[1])+1);
          var id_codEspol="SP-codEspol-"+(parseInt(nom[1])+1);
          var id_nombre="SP-nombre-"+(parseInt(nom[1])+1);
        }
        sel1.attr("id",id_codInv)
        tdCI.append(sel1);

        var sel2=$("<select>");
        sel2.attr("class","form-control select4 selectBien SP");
        sel2.attr("id",id_codEspol)
        tdCE.append(sel2);

        var sel3=$("<select>");
        sel3.attr("class","form-control select4 selectBien SP");
        sel3.attr("id",id_nombre)
        tdNB.append(sel3);

        // Inputs de bien_inventario

        var inFI=$("<input />")
        inFI.attr("class","form-control fecha_inventario");
        inFI.attr("type","date");
        tdFI.append(inFI);

        var selCO=$("<select>");
        selCO.attr("class","form-control select4 SP");
        // var hijosid=$("#productoTableBody").children();
        // if(hijosid.length==0){
        //   var id="SP-0";
        //   console.log("entro al if")
        // }else{
        //   console.log("entro al else")
        //   var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
        //   var id="SP-"+(parseInt(nom[1])+1);
        // }
        // selCO.attr("id",id)
        tdCO.append(selCO);
        
        var inOB=$("<input />")
        inOB.attr("class","form-control observacion");
        inOB.attr("type","text");
        tdOB.append(inOB);

        var inUR=$("<input />")
        inUR.attr("class","form-control usuario");
        inUR.attr("type","text");
        tdUR.append(inUR);

        var selSede=$("<select>");
        selSede.attr("class","form-control select4 SP");
        // var hijosid=$("#productoTableBody").children();
        // if(hijosid.length==0){
        //   var id="SP-0";
        //   console.log("entro al if")
        // }else{
        //   console.log("entro al else")
        //   var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
        //   var id="SP-"+(parseInt(nom[1])+1);
        // }
        // selSede.attr("id",id)
        tdSede.append(selSede);

        var inUB=$("<input />")
        inUB.attr("class","form-control observacion");
        inUB.attr("type","text");
        tdUB.append(inUB);

        var selES=$("<select>");
        selES.attr("class","form-control select4 SP");
        // var hijosid=$("#productoTableBody").children();
        // if(hijosid.length==0){
        //   var id="SP-0";
        //   console.log("entro al if")
        // }else{
        //   console.log("entro al else")
        //   var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
        //   var id="SP-"+(parseInt(nom[1])+1);
        // }
        // selES.attr("id",id)
        tdES.append(selES);

        var a=$("<a>");
        a.attr("class","btn btn-danger btn-sm eliminarFila");
        a.attr("href","#");
        var i=$("<i>");
        i.attr("class","fas fa-trash");
        a.append(i);
        tdA.append(a);

        fila.append(tdCI);
        fila.append(tdCE);
        fila.append(tdNB);
        fila.append(tdCA);
        fila.append(tdMA);
        fila.append(tdMO);
        fila.append(tdSE);
        fila.append(tdFI);
        fila.append(tdCO);
        fila.append(tdOB);
        fila.append(tdUR);
        fila.append(tdSede);
        fila.append(tdUB);
        fila.append(tdES);
        fila.append(tdA);

        $("#productoTableBody").append(fila);
        formatoSelect();
        load_bienes(sel1.attr("id"),bien,"cod_Inventariound");
        load_bienes(sel2.attr("id"),bien,"cod_bien");
        load_bienes(sel3.attr("id"),bien,"nombre");

        llenarSelectFila($(fila));
}

function llenarSelectFila(fila){
  var hijos = $(fila.children());
  $($(hijos[8]).children()[0]).html(opciones_selectores["constataciones"]);
  $($(hijos[11]).children()[0]).html(opciones_selectores["sedes"]);
  $($(hijos[13]).children()[0]).html(opciones_selectores["estados"]);
}

 $(document).on('click', '.eliminarFila', function () {
        var bien=$($(this).parent().parent().find("select")).val();
        console.log(bien);
        borrarFila(bien);
        $(this).parent().parent().remove();
 });

function cargarDatos(){
  var fila=0;
        $("#tableProSum tr").each(function(){
              var hijos=$(this).children();
              var cantidad=$(hijos[0]).find("input[type=number]").val();
              var precio=$(hijos[1]).find("input").val();
              var descuento=$(hijos[2]).find("input").val();
              var subtotal=$(hijos[3]).find("input").val();
              var producto=$(hijos[4]).find("select").val();
              var check=$(hijos[4]).find("input");
              console.log("Test");
              
              if(producto!=""){
                crearFila(producto);
                var hijos2=$("#productoTableBody").children();
                var lastf=hijos2[hijos2.length-1];
                var hijos3=$(lastf).children();
                $($(hijos3[6]).find("input")).val(cantidad);
                $($(hijos3[7]).find("input")).val(precio);
                $($(hijos3[8]).find("input")).val(descuento);
              }
              
              fila=fila+1
        });
}

function cargarDatosSelect() {
  var url = $('#Calificacion_proveedorForm').attr("data-select-url");
  $.ajax({
    url: url,
    data: {
    },
    success: function (data) {
        opciones_selectores["constataciones"] = data.constataciones;
        opciones_selectores["sedes"] = data.sedes;
        opciones_selectores["estados"] = data.estados;
    }
  });
}

function autocomplete(from, to) {
  if (from.val() != "") {
      $('#' + to).val(from.val()).trigger('change.select2');
  }
  else {
      $('#' + to).val(null).trigger('change.select2');
  }
}

cargarDatos();
cargarDatosSelect();

$("#id_tipo_bienes").on("change", function (e) {
  console.log($("#id_tipo_bienes").val())
  if ($("#id_tipo_bienes").val()=="") {
    console.log("Desactiva");
    $("#add").addClass("disabled");
  }
  else {
    console.log("Activa");
    $("#add").removeClass("disabled");
  }
  $("#id_bien").val(null).trigger('change');
  $("#productoTableBody").empty();
  load_data();
});