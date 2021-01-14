function DateToText(input) {
    if ($(input).val() == "") {
        $(input).attr("type", "text");
    }
}

function TextToDate(input) {
    if ($(input).val() != "") {
        const vars = $(input).val();
        const listv = vars.split("-");
        if (listv.length > 1) {
            const fechan = listv[0] + "-" + listv[1] + "-" + listv[2];
            $(input).val(fechan);
            $(input).attr("type", "date");
        }
    }
}