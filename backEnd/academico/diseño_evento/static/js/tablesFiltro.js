$(document).ready(function () {
    // Setup - add a text input to each footer cell
    $('#tablaDisenos thead tr').clone(true).appendTo('#tablaDisenos thead');
    $('#tablaDisenos thead tr:eq(1) th').each(function (i) {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Buscar" / style="width:100%">');

        $('input', this).on('keyup change', function () {
            if (table.column(i).search() !== this.value) {
                table
                    .column(i)
                    .search(this.value)
                    .draw();
            }
        });
    });

    var table = $('#tablaDisenos').DataTable({
        orderCellsTop: true,
        fixedHeader: true
    });

    $('#tablaArea').DataTable();
    $('#tablaEspecialidad').DataTable();
});


