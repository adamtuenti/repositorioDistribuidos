$("#PEtabla").children().each(function(){
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

    Object.keys(ccant).forEach(function(key){
        const span=$("<span>");
        span.html(key);
        $(cod).append(span);
        $(cod).append($("<br>"));

    });

   
    var valucant={}
    const val=$(this).children()[6];
    $(val).children().each(function(){
        if($(this).prop("tagName")!="BR"){
            if(valucant[$(this).attr("class")]!=undefined){
                valucant[$(this).attr("class")]=valucant[$(this).attr("class")] + parseFloat($(this).html());
                $(this).next().remove();
                $(this).remove();
            }else{
                valucant[$(this).attr("class")]=parseFloat($(this).html());
                $(this).next().remove();
                $(this).remove();
            }
        }
        
    });

    Object.keys(valucant).forEach(function(key){
        const span=$("<span>");
        span.html(transform(valucant[key]));
        $(val).append(span);
        $(val).append($("<br>"));

    });


});

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