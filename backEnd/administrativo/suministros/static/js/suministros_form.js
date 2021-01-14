
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
               $("#"+id).html(data.producto);
               if(proc!=null){
                $("#"+id).val(proc);
                $("#"+id).trigger("change");
               }
            }
          });
          
};




  $(document).on('change', '.SP', function () {
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
                    $(hijos[1]).html(data.unidad);
                    if(data.iva){
                        $(hijos[2]).html("Si");
                    }else{
                        $(hijos[2]).html("No");
                    }
                    $(hijos[3]).html(data.estado);
                    if(data.controlable){
                        $(hijos[4]).html("Si");
                    }else{
                        $(hijos[4]).html("No");
                    }
                    
                    $(hijos[5]).html(data.stock);
                    calcularSubtotal($("#"+idF));
                }
            });
        }else{
            console.log("borrar")
            var fila=$(this).parent().parent();
            var hijos= fila.children();
            $(hijos[1]).html("")
            $(hijos[2]).html("")
            $(hijos[3]).html("")
            $(hijos[4]).html("")
            $(hijos[5]).html("")
            $($(hijos[6]).children()[0]).val(null)
            $($(hijos[7]).children()[0]).val(null)
            $($(hijos[8]).children()[0]).val(null)
            $(hijos[9]).html("")
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
        var tdN=$("<td>");
        var tdU=$("<td>");
        var tdI=$("<td>");
        tdI.attr("class","iva");
        var tdE=$("<td>");
        var tdC=$("<td>");
        var tdS=$("<td>");
        var tdCA=$("<td>");
        var tdP=$("<td>");
        var tdD=$("<td>");
        var tdST=$("<td>");
        tdST.attr("class","subT");
        var tdA=$("<td>");


        var sel=$("<select>");
        sel.attr("class","form-control select4 SP");
        // var id="SP"+$("#productoTableBody").children().length
        var hijosid=$("#productoTableBody").children();
        if(hijosid.length==0){
          var id="SP-0";
          console.log("entro al if")
        }else{
          console.log("entro al else")
          var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
          var id="SP-"+(parseInt(nom[1])+1);
        }
        sel.attr("id",id)
        tdN.append(sel);

        var in1=$("<input />")
        in1.attr("class","form-control cantidad");
        in1.attr("type","number");
        tdCA.append(in1);
        
        var in2=$("<input />")
        in2.attr("class","form-control precio");
        in2.attr("placeholder","$");
        in2.attr("type","number");
        tdP.append(in2);

        var in3=$("<input />")
        in3.attr("class","form-control descuento");
        in3.attr("placeholder","%");
        in3.attr("type","number");
        tdD.append(in3);

        var a=$("<a>");
        a.attr("class","btn btn-danger btn-sm eliminarFila");
        a.attr("href","#");
        var i=$("<i>");
        i.attr("class","fas fa-trash");
        a.append(i);
        tdA.append(a);

        fila.append(tdN);
        fila.append(tdU);
        fila.append(tdI);
        fila.append(tdE);
        fila.append(tdC);
        fila.append(tdS);
        fila.append(tdCA);
        fila.append(tdP);
        fila.append(tdD);
        fila.append(tdST);
        fila.append(tdA);

        $("#productoTableBody").append(fila);
        formatoSelect();
        load_productos(sel.attr("id"),producto);
}

 $(document).on('click', '.eliminarFila', function () {
        var producto=$($(this).parent().parent().find("select")).val();
        console.log(producto);
        borrarFila(producto);
        $(this).parent().parent().remove();
        calcularTabla()
 });

 $(document).on('change', '.precio', function () {
        calcularSubtotal($(this));
});

$(document).on('change', '.cantidad', function () {
    calcularSubtotal($(this));
});

$(document).on('change', '.descuento', function () {
  var desc= $(this).val();
  if(desc<0){
      $(this).val(0);
  }else if(desc>100){
    $(this).val(100);
  }
    calcularSubtotal($(this));
});

function calcularSubtotal(node){
      var hijos=$(node).parent().parent().children();
      var producto=$($(hijos[0]).children()[0]).val();
      var cantidad=$($(hijos[6]).children()[0]).val();
      var precio=$($(hijos[7]).children()[0]).val();
      var descuento=$($(hijos[8]).children()[0]).val();
      var ivab=$($(hijos[2])).html();
      var subtotal=$(hijos[9]);
      
      console.log(ivab)
      if(producto!="" && cantidad!="" && precio!="" && descuento!="" ){
            if(ivab=="Si"){
                var total= cantidad*precio;
                var tdescuento= total - (total*descuento)/100;
                console.log(tdescuento)
                var tiva= tdescuento +(tdescuento*IVA)/100;
                console.log(tiva);
                $(subtotal).html(tiva);
                llenarFila(cantidad,precio,descuento,tiva,producto);
            }else{
              var total= cantidad*precio;
              var tdescuento= total - (total*descuento)/100;
              $(subtotal).html(tdescuento);
              console.log("entro aca")
              llenarFila(cantidad,precio,descuento,tdescuento,producto);
            }
            calcularTabla();
      }

}

function calcularTabla(){
  var subtotal=0;
  var ivaA=0;
  var total=0;
   $("#productoTableBody tr").each(function(){
        var cant=$(this).find(".cantidad").val();
        var precio=$(this).find(".precio").val();
        var desc=$(this).find(".descuento").val();
        var sub=parseFloat($(this).find(".subT").html());
        var iv=$(this).find(".iva").html();
        if(iv=="Si"){
          var t= cant*precio;
          var tdescuento= t - (t*desc)/100;
          var tiva=(tdescuento*IVA)/100;
          subtotal=subtotal+tdescuento;
          ivaA=ivaA+tiva
        }else{
          var t= cant*precio;
          var tdescuento= t - (t*desc)/100;
          subtotal=subtotal+tdescuento;
        }
        console.log(sub);
        total=parseFloat(total)+parseFloat(sub);
   });
   $("#sub_total").val(subtotal);
   $("#iva").val(ivaA);
   $("#valor_total").val(total);

   $("#id_subtotal").val(subtotal);
   $("#id_valor_iva").val(ivaA);
   $("#id_total").val(total);
}

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

cargarDatos();