

//Codigo para los archivos
$(document).on('change', ".ingresof", function (e) {
    e.preventDefault();
    console.log($(this).children([0]));
    const hijo=$(this).children([0]);
    console.log($(this).val());
    if($(this).val()==""){
        console.log("esta vacio");
        console.log($($(this).parent().children()[0]).attr("href"));
        if($($(this).parent().children()[0]).attr("href")==null){
            deleteForm('ordeningresofile_set', $(this));
        }
    }else{
        console.log("esta lleno");
        console.log($(".prueba:last input[type=file]"));
        if($(".prueba:last input[type=file]").val()!=""){
            cloneMore('.prueba:last', 'ordeningresofile_set');
        }
        /*  cantInput=cantInput+1;
        const divp=$("<div>");
        divp.attr("id","div_anexos"+cantInput);
        divp.attr("class","form-group");
        const inputf=$("<input/>");
        inputf.attr("type","file");
        inputf.attr("id","id_archivo"+cantInput);
        inputf.attr("class","form-control anexo");
        inputf.attr("name","archivo"+cantInput);
        $("#div_anexos").append(inputf);
        cont+=1;*/
    }
});

function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    var newrow=parseInt(total)+1
    newElement.attr("class","row"+(newrow) +" form-control prueba form-row formset_row-ordeningresofile_set")
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    
    newElement.find("input[type=hidden] + div").each(function(){
        $(this).attr("id","div_id_ordeningresofile_set-"+ (total)+"-file")
    });
    newElement.find("input[type=hidden] + div label").each(function(){
        $(this).attr("for","id_ordeningresofile_set-"+ (total)+"-file")
    });
    newElement.find("div[class=form-check]").attr("id","div_id_ordeningresofile_set-"+total+"-DELETE")
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);

}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        $(btn).parent().parent().parent().parent().remove();
        var forms = $('.prueba');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            console.log(forms[i]);
            console.log(i);
            $(forms.get(i)).find(':input[type=file]').each(function() {
                updateElementIndex(this, prefix, i,"-file");
            });
            var lol=0
            $(forms.get(i)).find(':input[type=hidden]').each(function() {
                if(lol==0){
                    updateElementIndex(this, prefix, i,"-id");
                    lol+=1;
                }else{
                    updateElementIndex(this, prefix, i,"-orden");
                }
            });
        }
        var formset= $(".formset_row-ordeningresofile_set");
        console.log(formset)
        for (var j=0, formsetCount=formset.length; j<formsetCount; j++) {
            console.log(formset[j]);
            var newrow=j+1
            console.log(newrow)
            $(formset.get(j)).attr("class","row"+newrow+"  form-control prueba form-row formset_row-ordeningresofile_set")
            var newElement=$(formset.get(j));

            newElement.find("input[type=hidden] + div").each(function(){
                $(this).attr("id","div_id_ordeningresofile_set-"+ (j)+"-file")
            });
            newElement.find("input[type=hidden] + div label").each(function(){
                $(this).attr("for","id_ordeningresofile_set-"+ (j)+"-file")
            });
            newElement.find("div[class=form-check]").attr("id","div_id_ordeningresofile_set-"+j+"-DELETE")
        }
    }
    return false;
}

function updateElementIndex(el, prefix, ndx, postfix) {
    
    var namep=prefix+"-"+(ndx)+postfix
    console.log(namep);
    var id = 'id_' + namep;
    $(el).attr('name', namep);
    $(el).attr('id', id);
    console.log($(el).attr('name'));
}


    if($("#id_cod_orden_ing").val()!=undefined){
        console.log("WTF")
        $("td a + input").each(function() {
            $(this).remove();
          });
        
          $("td a + label").each(function() {
            $(this).remove();
        });
    }else{
        console.log("registro");
        $("td input[type=checkbox]").each(function() {
            $(this).parent().remove();
            $(this).remove();
          });
          
    }

    $("tr label.col-form-label").text("Anexo")

