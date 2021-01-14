

//Codigo para los archivos
        $(document).on('change', ".anexo", function (e) {
            e.preventDefault();
            console.log($(this).children([0]));
            const hijo=$(this).children([0]);
            console.log($(this).val());
            if($(this).val()==""){
                console.log("esta vacio");
                console.log($($(this).parent().children()[0]).attr("href"));
                if($($(this).parent().children()[0]).attr("href")==null){
                    deleteForm('propuestafile_set', $(this));
                }
            }else{
                console.log("esta lleno");
                console.log($(".form-row:last input[type=file]"));
                if($(".form-row:last input[type=file]").val()!=""){
                    cloneMore('.form-row:last', 'propuestafile_set');
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
            newElement.attr("class","row"+(newrow) +" form-control form-row formset_row-propuestafile_set")
            newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
                var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
                var id = 'id_' + name;
                $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
            });
            
            newElement.find("input[type=hidden] + div").each(function(){
                $(this).attr("id","div_id_propuestafile_set-"+ (total)+"-file")
            });
            newElement.find("input[type=hidden] + div label").each(function(){
                $(this).attr("for","id_propuestafile_set-"+ (total)+"-file")
            });
            newElement.find("div[class=form-check]").attr("id","div_id_propuestafile_set-"+total+"-DELETE")
            total++;
            $('#id_' + prefix + '-TOTAL_FORMS').val(total);
            $(selector).after(newElement);
        
        }
        
        function deleteForm(prefix, btn) {
            var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
            if (total > 1){
                $(btn).parent().parent().parent().parent().remove();
                var forms = $('.form-row');
                $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length-1);
                for (var i=1, formCount=forms.length; i<formCount; i++) {
                    console.log(forms[i]);
                    $(forms.get(i)).find(':input[type=file]').each(function() {
                        updateElementIndex(this, prefix, i,"-file");
                    });
                    var lol=0
                    $(forms.get(i)).find(':input[type=hidden]').each(function() {
                        if(lol==0){
                            updateElementIndex(this, prefix, i,"-id");
                            lol+=1;
                        }else{
                            updateElementIndex(this, prefix, i,"-propuesta");
                        }
                    });
                }
                var formset= $(".formset_row-propuestafile_set");
                console.log(formset)
                for (var j=0, formsetCount=formset.length; j<formsetCount; j++) {
                    console.log(formset[j]);
                    var newrow=j+1
                    console.log(newrow)
                    $(formset.get(j)).attr("class","row"+newrow+"  form-control form-row formset_row-propuestafile_set")
                    var newElement=$(formset.get(j));

                    newElement.find("input[type=hidden] + div").each(function(){
                        $(this).attr("id","div_id_propuestafile_set-"+ (j)+"-file")
                    });
                    newElement.find("input[type=hidden] + div label").each(function(){
                        $(this).attr("for","id_propuestafile_set-"+ (j)+"-file")
                    });
                    newElement.find("div[class=form-check]").attr("id","div_id_propuestafile_set-"+j+"-DELETE")
                }
            }
            return false;
        }
        
        function updateElementIndex(el, prefix, ndx, postfix) {
            
            var namep=prefix+"-"+(ndx-1)+postfix
            console.log(namep);
            var id = 'id_' + namep;
            $(el).attr('name', namep);
            $(el).attr('id', id);
            console.log($(el).attr('name'));
        }
console.log($("[name=cod_propuesta]"))
    if($("[name=cod_propuesta]").val()!=""){
        $("td a + input").each(function() {
            $(this).remove();
          });
        
          $("td a + label").each(function() {
            $(this).remove();
        });
    }else{
        $("td input[type=checkbox]").each(function() {
            $(this).parent().remove();
            $(this).remove();
          });
        
          
    }

    $("tr label.col-form-label").text("Anexo")