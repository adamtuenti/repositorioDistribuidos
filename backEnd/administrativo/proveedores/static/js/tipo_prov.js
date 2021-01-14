function tipo_provee(){
    if(document.getElementById("id_tipo_proveedor").value = 'Natural'){

        document.getElementById("id_ruc").label.value = "CI";
        document.getElementById("id_razon").label.value = "Nombre";
        document.getElementById("id_div_ruc").style.display = inline;
        document.getElementById("id_div_razon").style.display = inline;

        
    }
    else if(document.getElementById("id_tipo_proveedor").value = 'Jurídica'){

        document.getElementById("id_ruc").label.value = "RUC";
        document.getElementById("id_razon").label.value = "Razón social";
        document.getElementById("id_div_ruc").style.display = inline;
        document.getElementById("id_div_razon").style.display = inline;
        
    }
}