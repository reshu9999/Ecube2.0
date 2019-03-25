$(document).ready(function ($) {
    bind_grid();
    $('#a_down').hide();
});
function Download_excel_templates() {
    window.location.href = '/static/Excel_Templates/lead_time.xlsx';
}
function bind_grid() {
    var count = $('#divradio_btn input:radio:checked').length;
    if (count == 0) {
        alert('Please select any radio option !!!')
        return false;
    }
    else {
        var id = $('#divradio_btn input:radio:checked')[0].id;
        var model = { id: id };
        $.ajax({
            url: Fgrid_bind_lead_time,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {

                Bind_grid_main(data.htl_grp_dtls)
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });


    }
}

function rest_frm() {
    window.location.href = window.location.href;
}

function Bind_grid_main(data) {

    var table = $("#datavalidation").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {
        trHTML += '<tr>' +
            '<td>' + item.Booking_date.split(' ')[0] + '</td>' +
            '<td>' + item.Batch_name + '</td>' +
            '<td>' + item.Destination + '</td>' +
            '<td>' + item.Lead_time_value + '</td>' +
            '<td>' + item.Event_time_value + '</td>' +
            '<td>' + item.Nights + '</td>' +
            '<td>' + item.NvcrAccountName + '</td>' +
            '<td>' + item.NvcrprimarysupplierName + '</td>' +
            '<td>' + item.smdtCheckindate.split('T')[0] + '</td>' +
            '</tr>'

    });
    $('#tbl_body_main_grp_list').append(trHTML);
    $('#datavalidation').dataTable({
        "sPaginationType": "full_numbers",
        "bFilter": true,
        "bInfo": false,
        "bPaginate": true,
        paging: true,
    });
    $('.dataTables_wrapper,.addhotel_checkbox_contaner').perfectScrollbar();
}
function Download_templet() {
    var count = $('#divradio_btn input:radio:checked').length;
    if (count == 0) {
        alert('Please select any radio option !!!')
        return false;
    }
    else {
        var id = $('#divradio_btn input:radio:checked')[0].id;
        var model = { id: id };
        $.ajax({
            url: File_download_excel_lead_time,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                if (data.count > 0) {
                    alert('file downloded successuly ');
                    window.location.href = data.Path
                }
                else {
                    alert("No record found on server !!!!!")
                }
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }

}
function upload_excel() {
    var count = $('#divradio_btn input:radio:checked').length;
    if (count == 0) {
        alert('Please select any radio option !!!')
        return false;
    }
    else {
        var file_val = $("#input_file_excel").val();
        if (file_val == '') {
            alert('Please select file and upload !!!');
            return false;
        }
        var id = $('#divradio_btn input:radio:checked')[0].id;
        var fileUpload = $("#input_file_excel").get(0);
        var files = fileUpload.files;
        var formdata = new FormData();
        formdata.append("File", files[0]);
        formdata.append("id", id);
        $.ajax({
            url: File_upload_excel_lead_time,
            type: "POST",
            processData: false,
            dataType: 'json',
            data: formdata,
            contentType: false,

            success: function (data) {
                $("#input_file_excel").val(null);
                $('.file_type').text('');
                $('.file_type').css('opacity', '0');
                if (data.count > 0) {
                    alert('Please  click on button for downloded  Error file !!!');
                    $('#a_down').show();
                    $('#a_down').attr("href", data.Path);
                }
                else {
                    $('#a_down').hide();
                    $('#a_down').attr("href", '');
                    alert(data.htl_grp_dtls);
                    bind_grid();
                }
            },


            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }

}


function Chk_name() {
    var id = $('#divradio_btn input:radio:checked')[0].id;
    if (id == 'lead_time') {
        $('#lbl_text').text('');
        $('#lbl_text').text('Lead Time Bulk Upload');
        $('#a_down').hide();
    }
    else {
        $('#lbl_text').text('');
        $('#lbl_text').text('Ad Hoc Time Bulk Upload');
        $('#a_down').hide();

    }
    bind_grid();
}
