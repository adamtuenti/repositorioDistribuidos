

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

$(document).on('click', '#add', function () {
    var hijos=$("#productoTableBody").children();
  
    var lastH=hijos[hijos.length-1];

    if(hijos.length==0){
      crearFila(null);
      cloneMoreMP('.pt:last', 'productosuministroegreso_set');
    }else{
      var sel= $($(lastH).children()[0]).find("select");
      console.log(sel);
      var cantS= $($(lastH).children()[5]).find("input");
      console.log(cantS);
      var cantD= $($(lastH).children()[6]).find("input");
      console.log(cantD);
      if($(sel).val()!="" && $(cantS).val()!="" && $(cantD).val()!=""){
        crearFila(null);
        cloneMoreMP('.pt:last', 'productosuministroegreso_set');
    }
  } 

  
});

function verificarFila(node){
        var val=$(node).val();
        var hijos= $(node).parent().parent().children();
        var sel= $(hijos[0]).find("select");
        var cantS= $(hijos[5]).find("input");
        var cantD= $(hijos[6]).find("input");
        if($(sel).val()!="" && $(cantS).val()!="" && $(cantD).val()!=""){
            llenarFila($(cantS).val(),$(cantD).val(),$(sel).val())
            console.log("entro")
        }else{
          console.log("no entro")
        }
        
}

$(document).on('click', '.eliminarFila', function () {
    var producto=$($(this).parent().parent().find("select")).val();
    console.log(producto);
    borrarFila(producto);
    $(this).parent().parent().remove();
    
});

$(document).on('change', '.cantidadS', function () {
  verificarFila(this);
});

$(document).on('change', '.cantidadD', function () {
  verificarFila(this);
});

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
                
                $(hijos[2]).html(data.estado);
                if(data.controlable){
                    $(hijos[3]).html("Si");
                }else{
                    $(hijos[3]).html("No");
                }
                
                $(hijos[4]).html(data.stock);
                verificarFila("#"+idF);
                
            }
        });
    }else{
        console.log("borrar")
        var fila=$(this).parent().parent();
        var hijos= fila.children();
        $(hijos[1]).html("");
        $(hijos[2]).html("");
        $(hijos[3]).html("");
        $(hijos[4]).html("");
        $($(hijos[5]).children()[0]).val(null)
        $($(hijos[6]).children()[0]).val(null)
    }
});

function crearFila(producto){
    var fila=$("<tr>");
    fila.attr("class","text-center")
    var tdN=$("<td>");
    var tdU=$("<td>");
    var tdE=$("<td>");
    var tdC=$("<td>");
    var tdS=$("<td>");
    var tdCS=$("<td>");
    var tdCD=$("<td>");
    var tdA=$("<td>");


    var sel=$("<select>");
    sel.attr("class","form-control select4 SP");
    var hijosid=$("#productoTableBody").children();
    if(hijosid.length==0){
      var id="SP-0";
      console.log("entro al if")
    }else{
      console.log("entro al else")
      var nom=$($(hijosid[hijosid.length-1]).find("select")).attr("id").split("-");
      var id="SP-"+(parseInt(nom[1])+1);
    }
    sel.attr("id",id);
    tdN.append(sel);

    var in1=$("<input />")
    in1.attr("class","form-control cantidadS");
    in1.attr("type","number");
    tdCS.append(in1);
    
    var in2=$("<input />")
    in2.attr("class","form-control cantidadD");
    in2.attr("type","number");
    tdCD.append(in2);


    var a=$("<a>");
    a.attr("class","btn btn-danger btn-sm eliminarFila");
    a.attr("href","#");
    var i=$("<i>");
    i.attr("class","fas fa-trash");
    a.append(i);
    tdA.append(a);

    fila.append(tdN);
    fila.append(tdU);
    fila.append(tdE);
    fila.append(tdC);
    fila.append(tdS);
    fila.append(tdCS);
    fila.append(tdCD);
    fila.append(tdA);

    $("#productoTableBody").append(fila);
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
    console.log
    load_productos(sel.attr("id"),producto);

}



function cargarDatos(){
  var fila=0;
        $("#tableProSum tr").each(function(){
              var hijos=$(this).children();
              var producto=$(hijos[0]).find("select").val();
              var cantS=$(hijos[1]).find("input").val();
              var cantD=$(hijos[2]).find("input").val();
              
              if(producto!=""){
                crearFila(producto);
                var hijos2=$("#productoTableBody").children();
                var lastf=hijos2[hijos2.length-1];
                var hijos3=$(lastf).children();
                $($(hijos3[5]).find("input")).val(cantS);
                $($(hijos3[6]).find("input")).val(cantD);
              }
              
              fila=fila+1
        });
}

cargarDatos();