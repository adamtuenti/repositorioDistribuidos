 async function load_ejecutados(year) {
    console.log(year);
    var tasas=0;
    var url = $('#form-espoltech').attr("data-ejecutados-url");
     await $.ajax({
        url: url,
        data: {
          'year': year,
          'centro': $("#tipoP").val(),
        },
        success: function (data) {
            var obj = JSON.parse(data);
            console.log(obj);
            //$("#id_ind_laborales_ejec").val("$"+obj["Indemnizaciones  Lab"]);
            Object.keys(obj).forEach(function(key){
              console.log(key);
              $('[gasto="'+key+'"]').val(obj[key]);
              $('[gasto="'+key+'"]').trigger("change");
            });
            tasas=obj["Tasas Generales, Impuestos. Contribuciones, Permisos, Licencias y Patentes (incluye aporte 5*1000)"];
            // $("#id_iva_ejec").val(obj["iva"]);
            // $("#id_iva_ejec").trigger("change");
        }
      });
      console.log(tasas);

      //Este ajax es para obtener los valores de ingresos corrientes, ingresos de financiamiento, tasa general y aportaciones
      url = $('#form-espoltech').attr("data-ejecutados-ingreso-aportaciones-url");
      var mensaje_exito = $("<p>Se ha actualizado el presupuesto de manera exitosa</p>");
      var mensaje_error = $("<p>Ha ocurrido un inconveniente, intentenlo más tarde</p>");
      var boton_entendido = $("<a id='boton_continuar'data-toggle='modal' data-target='#modal_confirmacion_actualizar' class='btn btn-success text-light float-right'> Continuar </a>");
      var div_modal_body = $("<div class = 'modal-body  id='modal_confirmacion_body'></div>")
      var todo_bien = $(div_modal_body).clone().append(mensaje_exito);
      var todo_mal = $(div_modal_body).clone().append(mensaje_error);

      $.ajax({
        url: url,
        data: {
          'year': year,
          'centro': $("#tipoP").val(),
        },
        beforeSend: function () {
          var loading = $("<img>")
          loading.addClass("img-fluid m-auto")
          loading.css({ "width": "50%", "height": "auto" })
          loading.attr("id", "id_loading")
          loading.attr('src', "https://miro.medium.com/max/1080/0*DqHGYPBA-ANwsma2.gif")
          $("#modal_confirmacion_actualizar .modal-content").html(loading);
        },
        success: function (data) {
            var obj = JSON.parse(data);
            console.log(data);
            //Ubicar los valores en los campos respectivos
            //En el caso que los valores incrementen en gran cantidad, se recomienda
            //seguir la logica del primer ajax.
            $("#id_vb_curs_sem_maes_ejec").val(transform(obj["total_facturacion_actual"]));
            $("#id_cta_x_cobrar_ejec").val(transform(obj["total_ording_actual"]));
            
            var tasa_acumulado = obj["tasa_general"] ;  
            if(tasas!= undefined){
              tasa_acumulado = tasa_acumulado + parseFloat(tasas);
            }
            $("#id_tasas_ejec").val(transform(tasa_acumulado));


            //ESPOLTECH
            console.log($("#tipoP").val());
            if($("#tipoP").val() ==="ESPOLTECH"){
              console.log("Actualice espoltech");
              $("#id_part_unidad_ejec").val(transform(obj["participacion_unidad"]));
              $("#id_espoltech_ep_ejec").val(transform(obj["centro_costo_ingresos"]));
              $("#id_part_espol_ejec").val(transform(obj["participacion_ingresos_espol"]));
              //Se disparan los eventos change para que los campos de valores ejecutados se sumen, esto se hace para que se ejecuten las funciones de espoltech_convar.js
              $("#id_part_unidad_ejec").trigger("change");
            }
            //FUNDESPOL
            else if($("#tipoP").val() ==="FUNDESPOL"){
              console.log("Actualice fundespol");
              $("#id_fundespol_ingresos_ejec").val(transform(obj["centro_costo_ingresos"]));
              $("#id_espol_ingresos_ejec").val(transform(obj["participacion_ingresos_espol"]));
              //Se disparan los eventos change para que los campos de valores ejecutados se sumen, esto se hace para que se ejecuten las funciones de espoltech_convar.js
              $("#id_fundespol_ingresos_ejec").trigger("change");
            }
            //Se disparan los eventos change para que los campos de valores ejecutados se sumen, esto se hace para que se ejecuten las funciones de espoltech_convar.js
            $("#id_cta_x_cobrar_ejec").trigger("change");
            $("#id_vb_curs_sem_maes_ejec").trigger("change");
            $("#id_tasas_ejec").trigger("change");
            //Agregar contenido al modal
            $("#modal_confirmacion_actualizar .modal-content").remove("img#id_loading");
            $("#modal_confirmacion_actualizar .modal-content").html(todo_bien.append(boton_entendido));

        },
        error:function(data){
          $("#modal_confirmacion_actualizar .modal-content").remove("img#id_loading");
          $("#modal_confirmacion_actualizar .modal-content").html(todo_mal.append(boton_entendido));
        }
        
      });
      
      
      
  };

  function transform(numero){
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
  function actualizar_campos(){
    const year=$("#id_año").val();
    console.log(year);

    Array.prototype.forEach.call($("#g_personal_div .ejec"), child => {
      $(child).val(transform(0));
    });

    Array.prototype.forEach.call($("#bs_consumo_div .ejec"), child => {
      $(child).val(transform(0));
    });

    Array.prototype.forEach.call($("#otros_gastos_corr_div .ejec"), child => {
      $(child).val(transform(0));
    });

    Array.prototype.forEach.call($("#act_fijos_div .ejec"), child => {
      $(child).val(transform(0));
    });

    if(year!="" && year>0 && year<10000){
      load_ejecutados($("#id_año").val());
    }
  }




  $("input#id_año").change(function (e) { 
    e.preventDefault();
    actualizar_campos();
  });
  
  $("a#actualizar_valores").click(function (e) { 
    e.preventDefault();
    actualizar_campos();
    
  });
  



