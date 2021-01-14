
console.log(localStorage.getItem("codigoevento"));
console.log($("#id_cod_evento").val());
if($("#id_cod_evento").val()==""){
    var ce=localStorage.getItem("codigoevento");
    $("#id_cod_evento").val(ce);

    // if (ce=="123"){
    //   $("#id_nombre_evento").val("Besto Evento");
    //   $("#id_valor_evento").val("1234567");
    // }else if(ce=="456"){
    //   $("#id_nombre_evento").val("Mas o Menos Evento");
    //   $("#id_valor_evento").val("420");
    // }else if(ce=="789"){
    //   $("#id_nombre_evento").val("The Worsto Evento");
    //   $("#id_valor_evento").val(30.45);
    // }else{
      var url = $('#form-participante').attr("data-evento-url");
      console.log("momazo")
      console.log(url)
      $.ajax({
        url: url,
        data: {
          'codigo': ce
        },
        success: function (data) {
          console.log(data.valor)
          $("#id_nombre_evento").val(data.nombre);
          $("#id_valor_evento").val(data.valor);
          $("#id_valor").val(data.valor);
          transform($("#id_valor_evento"));
          transform($("#id_valor"));
        }
      });
    // }

}

$("#id_cod_evento").prop("disabled",true);


$("#id_nombre_evento").prop("disabled",true);


$("#id_valor_evento").prop("disabled",true);


$(document).on('click', '#hack', function () {
    
    $("#id_cod_evento").prop("disabled",false);

    $("#id_nombre_evento").prop("disabled",false);

    $("#id_valor_evento").prop("disabled",false);
    const valmee=$("#id_valor_evento").val();
    $("#id_valor_evento").attr("type","number");
    $("#id_valor_evento").val(parseFloat(valmee.replace(/,/g,"")));
    $("#id_valor_evento").val(parseFloat($("#id_valor_evento").val()).toFixed(2));


    const val=$("#id_valor").val();
    $("#id_valor").attr("type","number");
    $("#id_valor").val(parseFloat(val.replace(/,/g,"")));
    $("#id_valor").val(parseFloat($("#id_valor").val()).toFixed(2));

  });


  function transform(input){
    if($(input).val()!=""){
      $(input).val(parseFloat($(input).val()).toFixed(2));
    $(input).attr("type","text");
   
    var numeroe=$(input).val().split(".")
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
    
    $(input).val("$"+newnum+"."+numeroe[1]);
    }
    
  }


  function load_participantes() {
    var url = $('#form-participante').attr("data-part-url");
      $.ajax({
        url: url,
        data: {
          'codigo': localStorage.getItem("codigoevento")
        },
        success: function (data) {
          $("#id_participante").html(data.participantes);
        }
      });
      
  };

  load_participantes();
  console.log("meme")