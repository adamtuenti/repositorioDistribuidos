$("tbody").children().each(function(){
    //Para los codigos del evento
    var ccant={};
    var codu=[];
    const cod=$(this).children()[5];
    $(cod).children().each(function(){
        if($(this).prop("tagName")!="BR"){
            if(codu.includes($(this).html())){
                ccant[$(this).html()]=ccant[$(this).html()]+1;
                $(this).next().remove();
                $(this).remove();
                
            }else{
                codu.push($(this).html());
                ccant[$(this).html()]=1;
                $(this).next().remove();
                $(this).remove();
            }
        }
        
    });
    console.log(ccant);
    console.log(codu);

    Object.keys(ccant).forEach(function(key){
        const span=$("<span>");
        span.html(key);
        $(cod).append(span);
        $(cod).append($("<br>"));

    });

    
    //Para los nombres de los eventos
    // var nomu=[];
    // const nom=$(this).children()[4];
    // $(nom).children().each(function(){
    //     if($(this).prop("tagName")!="BR"){
    //         if(nomu.includes($(this).attr("class"))){
    //             $(this).next().remove();
    //             $(this).remove();
                
    //         }else{
    //             nomu.push($(this).attr("class"));
    //         }
    //     }
        
    // });
    // console.log(nomu);
    var nomucant={}
    const nom=$(this).children()[4];
    $(nom).children().each(function(){
        if($(this).prop("tagName")!="BR"){
            if(nomucant[$(this).attr("class")]!=undefined){
                $(this).next().remove();
                $(this).remove();
            }else{
                nomucant[$(this).attr("class")]=$(this).html();
                $(this).next().remove();
                $(this).remove();
            }
        }
        
    });
    console.log(nomucant);
    Object.keys(nomucant).forEach(function(key){
        const span=$("<span>" ,{class: 'text-truncate'});
        span.html(nomucant[key]);
        $(nom).append(span);
        $(nom).append($("<br>"));

    });


    //subtotal para el descuento
    var subcant={}
    const subval=$(this).children()[6];
    $(subval).children().each(function(){
        if($(this).prop("tagName")!="BR"){
            if(subcant[$(this).attr("class")]!=undefined){
                subcant[$(this).attr("class")]=parseFloat($(this).html())+subcant[$(this).attr("class")];
            }else{
                subcant[$(this).attr("class")]=parseFloat($(this).html());
                console.log($(this).html())
            }
        }
        
    });
    console.log(subcant);

    const colsub=$(this).children()[8];
    Object.keys(subcant).forEach(function(key){
        const span=$("<span>");
        span.html(transform(subcant[key]));
        $(colsub).append(span);
        $(colsub).append($("<br>"));

    });


    //Para los valores de evento
    // var valu=[];
    // const val=$(this).children()[6];
    // $(val).children().each(function(){
    //     if($(this).prop("tagName")!="BR"){
    //         if(valu.includes($(this).html())){
    //             $(this).next().remove();
    //             $(this).remove();
    //         }else{
    //             valu.push($(this).html());
    //             $(this).html(transform($(this).html()))
    //         }
    //     }
        
    // });
    // console.log(valu);

    var valucant={}
    const val=$(this).children()[6];
    $(val).children().each(function(){
        if($(this).prop("tagName")!="BR"){
            if(valucant[$(this).attr("class")]!=undefined){
                $(this).next().remove();
                $(this).remove();
            }else{
                valucant[$(this).attr("class")]=parseFloat($(this).html());
                $(this).next().remove();
                $(this).remove();
            }
        }
        
    });
    console.log(subcant);

    Object.keys(valucant).forEach(function(key){
        const span=$("<span>");
        span.html(transform(valucant[key]));
        $(val).append(span);
        $(val).append($("<br>"));

    });

    //Para poner los participantes
    const part=$(this).children()[7];
    Object.keys(ccant).forEach(function(key){
        console.log(key);
        const span=$("<span>");
        span.html(ccant[key]);
        $(part).append(span);
        $(part).append($("<br>"));

    });

    //Para el valor total
    var vtcant={};
    const vt=$(this).children()[11];
    $(vt).children().each(function(){
        if($(this).prop("tagName")!="BR"){
            if(vtcant[$(this).attr("class")]!=undefined){
                vtcant[$(this).attr("class")]=parseFloat($(this).html())+vtcant[$(this).attr("class")];
                $(this).next().remove();
                $(this).remove();
            }else{
                vtcant[$(this).attr("class")]=parseFloat($(this).html());
                $(this).next().remove();
                $(this).remove();
            }
        }
        
    });
    console.log(vtcant);
    Object.keys(vtcant).forEach(function(key){
        console.log(key);
        const span=$("<span>");

        span.html(transform(vtcant[key]));
        
        $(vt).append(span);
        $(vt).append($("<br>"));

    });

    //Para el descuento
    const desc=$(this).children()[9];
    Object.keys(ccant).forEach(function(key){
        
        const span=$("<span>");
        var final=(subcant[key]-vtcant[key])/subcant[key]
        var ffinal= parseFloat(final*100).toFixed(2);
        span.html(ffinal+"%");
        $(desc).append(span);
        $(desc).append($("<br>"));

    });

    const descendolar=$(this).children()[10];
    Object.keys(ccant).forEach(function(key){
        
        const span=$("<span>");
        span.html(transform(subcant[key]-vtcant[key]))
        $(descendolar).append(span);
        $(descendolar).append($("<br>"));

    });



});

function transform(numero){
    var num=""+parseFloat(numero).toFixed(2);
    var numeroe=num.split(".")
    const long= numeroe[0].length;
    console.log(long)
    var newnum="";
    cont=0;
    for(var i=(long-1);i>=0;i--){
          if(cont%3==0 && cont!=0){
            newnum=numeroe[0].charAt(i)+","+newnum;
            console.log("coma");
            console.log(i);
            console.log(numeroe[0].charAt(i));
            cont+=1;
          }else{
            console.log("no coma");
            console.log(i);
            console.log(numeroe[0].charAt(i));
            newnum=numeroe[0].charAt(i)+newnum;
            cont+=1;
          }
    }
    console.log(newnum+"."+numeroe[1]);
    return "$"+newnum+"."+numeroe[1];
    
  }