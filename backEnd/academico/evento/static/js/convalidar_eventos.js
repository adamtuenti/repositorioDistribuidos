

  function guardar_convalidacion_historica() {
  	var ident = $('#identificacion').val();
  	var codigo_evento = $('#codigo_evento_historico').val();
  	var cbMotivo;
  	if ($('#motivo_standar').is(':checked')) {
  		cbMotivo = $('#motivo_standar').val();
  	}else{
  		cbMotivo = $('#motivo').val();
  	}

  	var conv_seleccion = $('#conv_seleccion').val();
  	var cod_evento_historico = $('#codigo_evento_historico').val();
  	var instituto_historico = $('#institucion_historico').val();
  	var archivo = $('#archivo_historico').val();
  }


  function buscar_evento(){
    if($('#identificacion').val().length >= 10 & $('#codigo').val().length >= 5){
        var dni = $('#identificacion').val();
        var cod = $('#codigo').val();
        var body_origen ='';
        fetch("../api_participantesEventos/",{
          method: 'POST',
          headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
          body: JSON.stringify({identificacion:dni,codigo:cod})
        })
        .then(res => res.json())
        .then(data => {
          console.log(data);
          $('#nombre_evento').val(data['nombre']);
          $('#estado').val(data['estado']);
          if (data['nombre'] != undefined) {
          body_origen += `
                     <tr id="filaEvento" scope="col">
                     		<th scope="col">1</th>
                			<th scope="col">${data.curso_codigo}</th>
                			<th scope="col">${data.nombre_curso}</th>
                			<th scope="col">${data.codigo_diseno}</th>
                			<th scope="col">${data.cod_programa}</th>
                			<th scope="col">${data.nombre}</th>
                			<th scope="col">${data.certificado_recibido}</th>
                			<th scope="col">${data.fecha_inicio}</th>
                			<th scope="col">${data.fecha_fin}</th>
                			<th scope="col">${data.duracion}</th>


            		</tr>
                    `;
         	$('#eventos_origen').html(body_origen);	
          }else{
        	$('#eventos_origen').empty();  	
          }
        })
      }
      else{
        $('#nombre_evento').val('');
        $('#estado').val('');
      	$('#eventos_origen').empty();
      }
  }


   function buscar_eventoDestino(){
    if($('#codigo_convalidar').val().length >= 5){
        var cod = $('#codigo_convalidar').val();
        var body = '';
        fetch("../EventosDestino/",{
          method: 'POST',
          headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
          body: JSON.stringify({codigo_convalidar:cod})
        })
        .then(res => res.json())
        .then(data => {
          console.log(data);
          $('#nombre_evento_convalidar').val(data['nombre']);
          $('#estado_convalidar').val(data['estado']);
           if (data['nombre'] != undefined) {
           		 body += `
                     <tr id="filaEvento" scope="col">
                     		<th scope="col">1</th>
                			<th scope="col">${data.curso_codigo}</th>
                			<th scope="col">${data.nombre_curso}</th>
                			<th scope="col">${data.codigo_diseno}</th>
                			<th scope="col">${data.cod_programa}</th>
                			<th scope="col">${data.nombre}</th>
                			<th scope="col">${data.certificado_recibido}</th>
                			<th scope="col">${data.fecha_inicio}</th>
                			<th scope="col">${data.fecha_fin}</th>
                			<th scope="col">${data.duracion}</th>
                			<th scope="col"><input type="submit" form="formulario_convalidacion" class="btn darkgreen-bg text-light float-right btn-block" value="Guardar" /></th>
            		</tr>
                    `;
            $('#eventos_destino').html(body);
           }else{
           	$("#eventos_destino").empty();
           }
        })
      }
      else{
        $('#nombre_evento_convalidar').val('');
        $('#estado_convalidar').val('');
        $("#eventos_destino").empty();
      }
  }

  function buscar_participante(){
    if($('#identificacion').val().length >= 10){
        var datos = $('#identificacion').val();
        fetch("../api_participantes/",{
          method: 'POST',
          headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
          body: JSON.stringify({identificacion:datos})
        })
        .then(res => res.json())
        .then(data => {
          //console.log(data);
          if (data['nombres'] == undefined) {
          	$('#nombre_participante').val('Identificación no registrada');
          }else{
          	 $('#nombre_participante').val(data['nombres']+" "+data['apellidos']);
          }
        })
      }
      else{
        $('#nombre_participante').val('');
      }
  }

  
