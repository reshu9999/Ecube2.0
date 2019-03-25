$(document).ready(function ($) {
    Bind_data_on_page_load();
    $('.multiselect_box').multiselect({
        includeSelectAllOption: true,
        buttonWidth: 250,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });
});

function Bind_data_on_page_load() {
    $.ajax({
        url: Bind_Country_name,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $(data.compt).each(function (index, item) {
                $('#drpCompt').append($('<option></option>').val(item.id).html(item.name));
            });
            $('#drpCompt').multiselect('rebuild')
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}

function reset()
{
    window.location.href=  window.location.href;
}

function bind_City_name_sup() {
    var sup_type = "";
    var selected_sup_type = $("#drpCompt option:selected");
    selected_sup_type.each(function () {
        sup_type += $(this).val() + ",";
    });
    sup_type = sup_type.replace(/,\s*$/, "").trim();
    if (sup_type != '') {
        var model = {
            sup_id: sup_type,
        };
        $.ajax({
            url: Bind_city_name_by_sup,
            type: 'POST',
            data: model,
            dataType: 'json',
            crossDomain: true,
            success: function (data) {
                $('#drp_cities').empty();
                $(data.City).each(function (index, item) {
                    $('#drp_cities').append($('<option></option>').val(item.id).html(item.cityname));
                });
                $('#drp_cities').multiselect('rebuild')
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }

}

function Bind_grid_sup_city() {
    var count = $('#divradio_btn input:radio:checked').length;
    if (count==0)
    {
        alert('Please select any radio button !!!');
        return false;
    }
    var sup_type = "";
    var selected_sup_type = $("#drpCompt option:selected");
    selected_sup_type.each(function () {
        sup_type += $(this).val() + ",";
    });
    sup_type = sup_type.replace(/,\s*$/, "").trim();
    var city_list = "";
    var city_drp = $("#drp_cities option:selected");
    city_drp.each(function () {
        city_list += $(this).val() + ",";
    });
    city_list = city_list.replace(/,\s*$/, "").trim();
    var id=$('#divradio_btn input:radio:checked')[0].id;
    if (sup_type=='')
    {
        alert('Please select any supplier name !!!');
        return false;
    }
    if (city_list=='')
    {
        alert('Please select any city  !!!');
        return false;
    }
        var model = {
            city_id: city_list,
            secondry_sup_id: sup_type,
            radio_id:id
        };
        var urls = 'https://'+SERVICES_IP+'/api/v1/sample/unmatched_sp_Bind_grid_for_match_unmatch_download_excel'
        $.ajax({
            url: urls ,
            type: 'GET',
            data: model,
            dataType: 'json',
            crossDomain: true,
            beforeSend: function(){
                $('.loader_div').show();
                },
            success: function (data) {
                if (data.count== 0)
                {
                    alert('No record found on server !!!!')
                }
        
                if (id=='exact_match')
                {
                    $('#div_exact').show();
                    $('#div_unmatch').hide();
                    $('#div_prob').hide();
                    setData_htls_detals_exact(data.data.data)
                }
                else if (id=='probable_match')
                {
                    $('#div_prob').show();
                    $('#div_exact').hide();
                    $('#div_unmatch').hide();
                    setData_htls_detals_prob(data.data.data)
                }
                else if (id=='unmatch_data')
                {
                    $('#div_unmatch').show();
                    $('#div_exact').hide();
                    $('#div_prob').hide();
                    setData_htls_detals_unmatch(data.data.data)
                }
            },
            complete:function(data){
                $('.loader_div').hide();
       },
            error: function (xhr, errorType, exception) {
                alert(exception);
            }
        });
}

function setData_htls_detals(data) {
    $('#div_table').show();
    var table = $("#datavalidation").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {

        trHTML+=' <tr >' +
            '                                      <td>' + item.code + '</td>' +
            '                                      <td>' + item.Primary_hotel_name + '</td>' +
            '                                      <td><span class="circle red">Inactive</span></td>' +
            '                                      <td> <span class="text-uppercase">Saraca Estate 19 Mall Ave..</span></td>' +
            '                                      <td>' + item.long + '</td>' +
            '                                      <td>' + item.lat + '</td>' +
            '                                      <td><span class="text-uppercase">' + item.sup_name + '</span></td>' +
            '                                    </tr>'


    });
    $('#tbody_selec_grid_second').append(trHTML);
    $('#datavalidation').dataTable( {
      "sPaginationType": "full_numbers",
		"bFilter": true,
		"bInfo": false,
		"bPaginate": true,
        paging: true,
	});
    $('.dataTables_scrollBody,.addhotel_checkbox_contaner').perfectScrollbar();

}


function setData_htls_detals_exact(data) {
    var table = $("#datavalidation_exact").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {

        trHTML+=' <tr >' +
            '<td>' + item[0]+ '</td>' +
            '<td>' + item[1]+ '</td>' +
            '<td>' + item[2]+ '</td>' +
            '<td>' + item[3]+ '</td>' +
            '<td>' + item[4]+ '</td>' +
            '<td>' + item[5]+ '</td>' +
            '<td>' + item[6]+ '</td>' +
            '<td>' + item[7]+ '</td>' +
            '<td>' + item[8]+ '</td>' +
            '<td>' + item[9]+ '</td>' +
            '<td>' + item[10]+ '</td>' +
            '<td>' + item[11]+ '</td>' +
            '<td>' + item[12]+ '</td>' +
            '<td>' + item[13]+ '</td>' +
            '<td>' + item[14]+ '</td>' +
            '<td>' + item[15]+ '</td>' +
            '<td>' + item[16]+ '</td>' +
            '<td>' + item[17]+ '</td>' +
            '<td>' + item[18]+ '</td>' +
            '<td>' + item[19]+ '</td>' +
            '<td>' + item[20]+ '</td>' +
            '<td>' + item[21]+ '</td>' +
            '<td>' + item[22]+ '</td>' +
            '<td>' + item[23]+ '</td>' +
            '<td>' + item[24]+ '</td>' +

            '</tr>'


    });
    $('#tbody_selec_grid_second_exact').append(trHTML);
    $('#datavalidation_exact').dataTable( {
      "sPaginationType": "full_numbers",
		"bFilter": true,
		"bInfo": false,
		"bPaginate": true,
        paging: true,
	});
    $('.dataTables_scrollBody,.addhotel_checkbox_contaner').perfectScrollbar();

}


function setData_htls_detals_unmatch(data) {
    var table = $("#datavalidation_unmatch").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {

        trHTML+=' <tr >' +
            '<td>' + item[0]+ '</td>' +
            '<td>' + item[1]+ '</td>' +
            '<td>' + item[2]+ '</td>' +
            '<td>' + item[3]+ '</td>' +
            '<td>' + item[4]+ '</td>' +
            '<td>' + item[5]+ '</td>' +
            '<td>' + item[6]+ '</td>' +
            '<td>' + item[7]+ '</td>' +
            '<td>' + item[8]+ '</td>' +
            '<td>' + item[9]+ '</td>' +
            '<td>' + item[10]+ '</td>' +
            '<td>' + item[11]+ '</td>' +
            '<td>' + item[12]+ '</td>' +
            '</tr>'


    });
    $('#tbody_selec_grid_second_unmatch').append(trHTML);
    $('#datavalidation_unmatch').dataTable( {
      "sPaginationType": "full_numbers",
		"bFilter": true,
		"bInfo": false,
		"bPaginate": true,
        paging: true,
	});
    $('.dataTables_scrollBody,.addhotel_checkbox_contaner').perfectScrollbar();

}



function setData_htls_detals_prob(data) {
    var table = $("#datavalidation_prob").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {

        trHTML+=' <tr >' +
            '<td>' + item[0]+ '</td>' +
            '<td>' + item[1]+ '</td>' +
            '<td>' + item[2]+ '</td>' +
            '<td>' + item[3]+ '</td>' +
            '<td>' + item[4]+ '</td>' +
            '<td>' + item[5]+ '</td>' +
            '<td>' + item[6]+ '</td>' +
            '<td>' + item[7]+ '</td>' +
            '<td>' + item[8]+ '</td>' +
            '<td>' + item[9]+ '</td>' +
            '<td>' + item[10]+ '</td>' +
            '<td>' + item[11]+ '</td>' +
            '<td>' + item[12]+ '</td>' +
            '<td>' + item[13]+ '</td>' +
            '<td>' + item[14]+ '</td>' +
            '<td>' + item[15]+ '</td>' +
            '<td>' + item[16]+ '</td>' +
            '<td>' + item[17]+ '</td>' +
            '<td>' + item[18]+ '</td>' +
            '<td>' + item[19]+ '</td>' +
            '<td>' + item[20]+ '</td>' +
            '<td>' + item[21]+ '</td>' +
            '<td>' + item[22]+ '</td>' +
            '<td>' + item[23]+ '</td>' +
            '<td>' + item[24]+ '</td>' +
            '<td>' + item[25]+ '</td>' +
            '<td>' + item[26]+ '</td>' +
            '<td>' + item[27]+ '</td>' +
            '</tr>'


    });
    $('#tbody_selec_grid_second_prob').append(trHTML);
    $('#datavalidation_prob').dataTable( {
      "sPaginationType": "full_numbers",
		"bFilter": true,
		"bInfo": false,
		"bPaginate": true,
        paging: true,
	});
    $('.dataTables_scrollBody,.addhotel_checkbox_contaner').perfectScrollbar();

}

function download_excel(){
    var count = $('#divradio_btn input:radio:checked').length;
    if (count==0)
    {
        alert('Please select any radio button !!!');
        return false;
    }
    var sup_type = "";
    var selected_sup_type = $("#drpCompt option:selected");
    selected_sup_type.each(function () {
        sup_type += $(this).val() + ",";
    });
    sup_type = sup_type.replace(/,\s*$/, "").trim();
    var city_list = "";
    var city_drp = $("#drp_cities option:selected");
    city_drp.each(function () {
        city_list += $(this).val() + ",";
    });
    city_list = city_list.replace(/,\s*$/, "").trim();
   
    var id=$('#divradio_btn input:radio:checked')[0].id;

    if (sup_type=='')
    {
        alert('Please select any supplier name !!!');
        return false;
    }
    if (city_list=='')
    {
        alert('Please select any city  !!!');
        return false;
    }
   
           var model = {
            city_id: 1,
            secondry_sup_id: 2,
            radio_id :id
        };
        $.ajax({
            url:  'https://'+SERVICES_IP+'/api/v1/sample/sp_Bind_grid_for_Sec_popup_for_excel',
            type: 'GET',
            data: model,
            dataType: 'json',
            crossDomain: true,
            success: function (data) {
                if (data.data.path!='0') {
                    data.data.path = 'https://'+SERVICES_IP +data.data.path;
                    window.location.href = data.data.path;
                }
                else
                {
                    alert('No data found on server !!!');
                }
            },
            error: function (xhr, errorType, exception) {
                alert(exception);
            }
        });
   
}
