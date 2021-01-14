$(document).on('focusout',".money input",function () {
    $(this).attr("type", "text").val(formatNumber($(this).val())).addClass("pr-3");
});



$(document).on('focus',".money input",function () {
    const r = unformatNumber($(this).val());
    $(this).attr("type", "number").removeClass("pr-3").val(r);
});

function unformatNumber(input) {
    var val = input;
    
    if (val !== "" && isNaN(val)) {
        var result = (+val.replace(/,/g,"")).toFixed(2);
        return result
    }
    return +val;
}

function formatNumber(input) {
    var val = input;
    
    if (val != "" ) {
        val = (+val).toFixed(2)
        var numeroe = val.split(".")
        const long = numeroe[0].length;
        var newnum = "";
        cont = 0;
        for (var i = (long - 1); i >= 0; i--) {
            if (cont % 3 == 0 && cont != 0) {
                newnum = numeroe[0].charAt(i) + "," + newnum;
                cont += 1;
            } else {
                newnum = numeroe[0].charAt(i) + newnum;
                cont += 1;
            }
        }
        return newnum + "." + numeroe[1];
    }

    return "0.00";
}