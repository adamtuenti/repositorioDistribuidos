cont=0;
$("#listaP").children().each(function(){
    if(cont!=0){
        $(this).find(".numO").html(cont);
    }
    cont=cont+1;
});

cont2=0
$("#listaEP").children().each(function(){
    if(cont2!=0){
        var cod=$(this).find(".nombreEP").attr("id");
        var url = $('#listaEP').attr("data-part-url");
        $.ajax({
            url: url,
            data: {
                'cod_evento': cod,
              },
            success: function (data) {
                const part=data.participantes;
                const code=data.codigo;
                console.log(part)
                console.log(cod)
                idr="#reg"+code
                idp="#pen"+code
                idq="#eq"+code
                $(idr).html(part);
                var equilibrio= $(idq).html();
                pendiente=parseInt(equilibrio)-part;
                if(pendiente<=0){
                    $(idp).html(0)
                }else{
                    $(idp).html(pendiente)
                    mitad=Math.ceil(parseInt(equilibrio)/2);
                    console.log(mitad)
                    if(pendiente>=mitad){
                        $(idp).css('color', 'red');
                    }
                }


            }
        });
    }
    cont2=cont2+1;
});
console.log("cambio")