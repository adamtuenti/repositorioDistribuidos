$('.select3').select2({  
    tags: true,
    dropdownParent: $("#ParticipantesModal").parent(),
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


function cargar_personas(){
    var url = $('#codigoEasy').attr("data-natural-url");
    console.log(url);
    console.log($("#codigoEasy").html());
      $.ajax({
        url: url,
        data: {
            'codigo': $("#codigoEasy").html(),
          },
        success: function (data) {
            $("#cedulaAP").html(data.cedula);
            $("#nombreAP").html(data.nombre);
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

$(document).on('change', '#cedulaAP', function () {
    autocomplete($(this), 'nombreAP');
    var cedula=$("#cedulaAP").val();
    if(cedula!="" && verificarParticipante(cedula) && verficarCambPart()){
        agregarParticipanteTabla(cedula,$("#nombreAP").val(),true);
    }
 });

 $(document).on('change', '#nombreAP', function () {
    autocomplete($(this), 'cedulaAP');
    var cedula=$("#cedulaAP").val();
    if(cedula!="" && verificarParticipante(cedula) && verficarCambPart()){
        agregarParticipanteTabla(cedula,$("#nombreAP").val(),true);
    }
 });

 $(document).on('click', '.eliminarNatural', function () {
    $(this).parent().parent().remove();
 });


 function verficarCambPart(){
   if($("#id_categoria").val()=="Part" && $("#id_tipo_nota").val()=="Crédito"){
        var hijos= $("#tablaNatural").children();
        console.log(hijos.length);
        if(hijos.length==1){
          console.log("entro a false");
          return false;
        }

   }
   console.log("entro a true");
   return true;
 }


 contI=0;
 $(document).on('click', '#agregar', function () {

    if(contI==0){
        $("#tablaNatural").children().each(function(){
            var cols=$(this).children();
            var cedula=$(cols[0]).html();
            console.log(cedula);
            var nombre=$(cols[1]).html();
            var total = $('#id_procesoparticipante_set-TOTAL_FORMS').val();
            console.log($(cols[2]).html());
            if($(cols[2]).html()!=''){
                $("#id_procesoparticipante_set-"+(total-1)+"-participante").val(cedula);
                $("#id_procesoparticipante_set-"+(total-1)+"-nombre_evento").val($("#nombreEvento").val());
                $("#id_procesoparticipante_set-"+(total-1)+"-cod_evento").val($("#codigoEvento").val());
        
                var valor=$("#id_valor_eventoC").val();
                var valorT=parseFloat(valor.replace(/,/g,"")).toFixed(2);
                console.log(valorT)
                var desc=$("#id_descuentoC").val();
                console.log(desc);
                var subtotal=valorT-(valorT*desc)/100;
                console.log(subtotal);
                $("#id_procesoparticipante_set-"+(total-1)+"-valor_evento").val(valorT);
                $("#id_procesoparticipante_set-"+(total-1)+"-descuento").val(desc);
                $("#id_procesoparticipante_set-"+(total-1)+"-valor").val(subtotal);
                $("#MEGAHACK").trigger("click");
            }
                
        });
        $("#MEGAHACK").trigger("actualizar");
        contI=1
    }
    
 });


function agregarParticipanteTabla(ced,nom,eliminar){
    var row=$("<tr>");
    row.attr("class","text-center");
    var cedula=$("<td>");
    var nombre=$("<td>");
    var acciones=$("<td>");

    var a=$("<a>");
    a.attr("class","btn btn-danger btn-sm eliminarNatural");
    a.attr("href","#");
    var i=$("<i>");
    i.attr("class","fas fa-trash");
    a.append(i);

    cedula.html(ced);
    nombre.html(nom);

    if(eliminar){
        acciones.append(a);
    }
    

    row.append(cedula);
    row.append(nombre);
    row.append(acciones);

    $("#tablaNatural").append(row);
    var tipo=$("#id_categoria").val();
    if (tipo==""){
      tipo=$("#catLazy").val();
    }
    if(tipo=="Grat" && eliminar){
      var url = $('#codigoEasy').attr("data-alertaCG-url");
      $.ajax({
        url: url,
        data: {
            'codigo': $("#codigoEasy").html(),
            'cedula':ced,
            'nombre':nom,
          },
        success: function (data) {
          console.log("entro a la alerta")
            if (data.alerta){
              alert("El participante "+data.nombre+" ya ha visto un evento con el mismo codigo de diseño")
            }
        }
      });
    }
}

function verificarParticipante(cedula){
    var rows=$("#tablaNatural").children();
    bandera=true;
    $(rows).each(function(){
         var cols=$(this).children();
         var ced=$(cols[0]).html();
         if(cedula==ced){
            bandera=false;
         }
    });
    return bandera;
}

cargar_personas();

$("#tbodyPart tr").each(function(){
    var children=$(this).children();
    var codigo= $(children[2]).html();

    var participante=$(children[0]).html();
    var cedula=participante.split(" ")[0];
    var nombre=participante.split("-")[1].replace(" ","");
    if(codigo==$("#codigoEasy").html()){
            agregarParticipanteTabla(cedula,nombre,false);
    }
});

console.log("NUEVAS WEAS");