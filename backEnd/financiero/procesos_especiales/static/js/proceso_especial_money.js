//seccion de signo de dolar
var monto=$("#div_id_valor_eventoC");
var inp=$("#div_id_valor_eventoC input");
var hijos=monto.children();
var d=hijos[1];
d.remove();
var dollar=$("<div>");
dollar.attr("class","input-icon")
var icono=$("<i>");
icono.text("$");
dollar.append(inp);
dollar.append(icono);
monto.append(dollar);

