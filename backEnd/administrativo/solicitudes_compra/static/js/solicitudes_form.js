
const IVA=12;

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
      
    
function load_productos(id,proc) {

        var url = $('#Calificacion_proveedorForm').attr("data-producto-url");
          $.ajax({
            url: url,
            success: function (data) {
              console.log(data.producto,id);
               $("#"+id).html(data.producto);
               if(proc!=null){
                $("#"+id).val(proc);
                $("#"+id).trigger("change");
               }
            }
          });
          
};

function load_opciones(id) {
  var opciones ='<option value="">---------</option><option value="2" name="">Productos </option><option value="1" name="">Otro </option>';
  $("#"+id).html(opciones);
}


$(document).on('change', '.SP', function () {
      var id=$(this).val();
      if(id!=""){
          var idFP=$(this).attr("id");
          // Select 2nd col (tdT)
          var node = $("#"+idFP+"I");
          // Create new td
          var tdI=$("<td>");
          tdI.attr("id",idFP+"I");

          var fila=$(this).parent().parent();
          var hijos= fila.children();

          if(id=="2") {
            var sel=$("<select>");
            sel.attr("class","form-control select4 prod");
            var id_select = idFP+"Isel";
            sel.attr("id",id_select)
            
            // Replace old td with new td
            tdI.append(sel);
            node.replaceWith(tdI);
            formatoSelect()
            load_productos(sel.attr("id"),null);
          }
          else if(id=="1") {
            var in_otros=$("<input />")
            in_otros.attr("class","form-control otros");
            in_otros.attr("type","text");

            // Replace old td with new td
            tdI.append(in_otros);
            node.replaceWith(tdI);

            // Unidades
            var in_units=$("<input />")
            in_units.attr("class","form-control unidades");
            in_units.attr("type","text");

            // Replace old td with new td
            $(hijos[2]).html(in_units);

            // Tiene IVA
            var sel=$("<select>");
            sel.attr("class","form-control select4 iva_select");
            sel.attr("id",id + "IVA");
            
            // Replace old td with new td
            $(hijos[10]).html(sel);
            formatoSelect();
            var opciones ='<option value="2" name="">Si</option><option value="1" name="">No</option>';
            $("#"+id + "IVA").html(opciones);            
          }
      }else{
          console.log("borrar")
          var fila=$(this).parent().parent();
          var hijos= fila.children();
          $(hijos[1]).html("");
          $(hijos[2]).html("");
          $(hijos[3]).html("");
          $(hijos[4]).html("");
          $(hijos[5]).html("");
          $(hijos[6]).html("");
          $(hijos[7]).html("");
          $($(hijos[8]).children()[0]).val(null);
          $($(hijos[9]).children()[0]).val(null);
          $(hijos[10]).html("");
          $(hijos[11]).html("");
      }
});

$(document).on('change', '.prod', function () {
 var id=$(this).val();
        if(id!=""){
            var idFP=$(this).attr("id");
            var url = $('#Calificacion_proveedorForm').attr("data-productoInd-url");
            $.ajax({
                url: url,
                data:{
                    'id':id,
                    'idF':idFP
                },
                success: function (data) {
                    var idF=data.idF;
                    var fila=$("#"+idF).parent().parent();
                    var hijos= fila.children();
                    console.log(fila)
                    $(hijos[2]).html(data.unidad);
                    if(data.iva){
                        $(hijos[10]).html("Si");
                    }else{
                        $(hijos[10]).html("No");
                    }                    
                    $(hijos[5]).html(data.stock);
                    $(hijos[6]).html(data.punto_reorden);
                    $(hijos[7]).html(data.stock-data.punto_reorden);
                    calcularSubtotal($("#"+idF));
                }
            });
        }else{
          console.log("borrar")
          var fila=$(this).parent().parent();
          var hijos= fila.children();
          $(hijos[2]).html("");
          $(hijos[3]).html("");
          $(hijos[4]).html("");
          $(hijos[5]).html("");
          $(hijos[6]).html("");
          $(hijos[7]).html("");
          $($(hijos[8]).children()[0]).val(null);
          $($(hijos[9]).children()[0]).val(null);
          $(hijos[10]).html("");
          $(hijos[11]).html("");
        }
 });

$(document).on('click', '#add', function () {
    var hijos=$("#productoTableBody").children();
    var lastH=hijos[hijos.length-1];
    var sub=$($(lastH).children()[9]).html();
    if(sub!=''){
      crearFila(null);
      cloneMoreM('.pt:last', 'productosuministro_set');
    }
      

    
 });

function crearFila(producto){
        var fila=$("<tr>");
        fila.attr("class","text-center")
        var tdT=$("<td>");
        var tdI=$("<td>");
        var tdU=$("<td>");
        var tdPP=$("<td>");
        var tdC=$("<td>");
        var tdSA=$("<td>");
        var tdPR=$("<td>");
        var tdSR=$("<td>");
        var tdCA=$("<td>");
        var tdPRE=$("<td>");
        var tdIVA=$("<td>");
        tdIVA.attr("class","iva");
        var tdST=$("<td>");
        tdST.attr("class","tot");
        var tdA=$("<td>");


        var sel=$("<select>");
        sel.attr("class","form-control select4 SP");
        // var id="SP"+$("#productoTableBody").children().length
        var hijosid=$("#productoTableBody").children();
        console.log("agrego fila")
        if(hijosid.length==0){
          var id="SP-0";
          console.log("entro al if")
        }else{
          console.log("entro al else")
          var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
          var id="SP-"+(parseInt(nom[1])+1);
        }
        sel.attr("id",id)
        tdT.append(sel);
        tdI.attr("id",id+"I");

        var sel2=$("<select>");
        sel2.attr("class","form-control select4 SP");
        sel2.attr("id",id + "PP");
        tdPP.append(sel2);

        var in1=$("<input />")
        in1.attr("class","form-control cantidad");
        in1.attr("type","number");
        tdCA.append(in1);
        
        var in2=$("<input />")
        in2.attr("class","form-control precio");
        in2.attr("placeholder","$");
        in2.attr("type","number");
        tdPRE.append(in2);

        var in3=$("<input />")
        in3.attr("class","form-control caracteristicas");
        in3.attr("type","text");
        tdC.append(in3);

        var a=$("<a>");
        a.attr("class","btn btn-danger btn-sm eliminarFila");
        a.attr("href","#");
        var i=$("<i>");
        i.attr("class","fas fa-trash");
        a.append(i);
        tdA.append(a);

        fila.append(tdT);
        fila.append(tdI);
        fila.append(tdU);
        fila.append(tdPP);
        fila.append(tdC);
        fila.append(tdSA);
        fila.append(tdPR);
        fila.append(tdSR);
        fila.append(tdCA);
        fila.append(tdPRE);
        fila.append(tdIVA);
        fila.append(tdST);
        fila.append(tdA);

        $("#productoTableBody").append(fila);
        formatoSelect();
        load_opciones(sel.attr("id"));
        //load_partidas(sel2.attr("id"));
}

 $(document).on('click', '.eliminarFila', function () {
        var producto=$($(this).parent().parent().find("select")).val();
        console.log("Borrando fila");
        borrarFila(producto);
        $(this).parent().parent().remove();
        calcularTabla()
 });

 $(document).on('change', '.precio', function () {
        calcularSubtotal($(this));
});

$(document).on('change', '.cantidad', function () {
  var cant= $(this).val();
  if(cant<0){
      $(this).val(0);
  }
    calcularSubtotal($(this));
});

$(document).on('change', '.iva_select', function () {
    calcularSubtotal($(this));
});

function calcularSubtotal(node){
      var hijos=$(node).parent().parent().children();
      var producto=$($(hijos[1]).children()[0]).val();
      var cantidad=$($(hijos[8]).children()[0]).val();
      var precio=$($(hijos[9]).children()[0]).val();
      var ivab=$($(hijos[10])).html();
      if($(hijos[10]).find(".iva_select").is( "select" )) {
        ivab = $(hijos[10]).find(".iva_select :selected").text();
      }
      console.log(ivab);
      var subtotal=$(hijos[11]);
      
      console.log(ivab)
      if(producto!="" && cantidad!="" && precio!="" ){
            if(ivab=="Si"){
                var total= cantidad*precio;
                var tiva= total +(total*IVA)/100;
                console.log(tiva);
                $(subtotal).html(tiva);
                llenarFila(cantidad,precio,tiva,producto);
            }else{
              var total= cantidad*precio;
              $(subtotal).html(total);
              console.log("entro aca")
              llenarFila(cantidad,precio,total,producto);
            }
            calcularTabla();
      }

}

function calcularTabla(){
  var subtotal_0=0;
  var subtotal_iva=0;
  var ivaA=0;
  var total=0;
   $("#productoTableBody tr").each(function(){
        var cant=$(this).find(".cantidad").val();
        var precio=$(this).find(".precio").val();
        var sub=parseFloat($(this).find(".tot").html());
        var iv=$(this).find(".iva").html();
        if($(this).find(".iva_select").is( "select" )) {
          iv = $(this).find(".iva_select :selected").text();
        }
        var subtotal= cant*precio;
        if(iv=="Si"){
          var tiva=(subtotal*IVA)/100;
          ivaA=ivaA+tiva;
          subtotal_iva=subtotal_iva+subtotal;
        }
        else{
          subtotal_0=subtotal_0+subtotal;
        }
        total=parseFloat(total)+parseFloat(sub);
   });
   $("#sub_total_0").val(subtotal_0);
   $("#sub_total_iva").val(subtotal_iva);
   $("#iva").val(ivaA);
   $("#valor_total").val(total);

   $("#id_subtotal_0").val(subtotal_0);
   $("#id_subtotal_iva").val(subtotal_iva);
   $("#id_valor_iva").val(ivaA);
   $("#id_total").val(total);
}

function cargarDatos(){
  var fila=0;
        $("#tableProSum tr").each(function(){
              var hijos=$(this).children();
              var cantidad=$(hijos[0]).find("input[type=number]").val();
              var precio=$(hijos[1]).find("input").val();
              var subtotal=$(hijos[3]).find("input").val();
              var producto=$(hijos[4]).find("select").val();
              var check=$(hijos[4]).find("input");
              
              if(producto!=""){
                crearFila(producto);
                var hijos2=$("#productoTableBody").children();
                var lastf=hijos2[hijos2.length-1];
                var hijos3=$(lastf).children();
                $($(hijos3[6]).find("input")).val(cantidad);
                $($(hijos3[7]).find("input")).val(precio);
              }
              
              fila=fila+1
        });
}

cargarDatos();