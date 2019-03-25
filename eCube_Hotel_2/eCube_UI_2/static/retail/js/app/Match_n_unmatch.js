$(document).ready(function ($) {
    Bind_data_on_page_load();
    $('.multiselect_box').multiselect({
        includeSelectAllOption: true,
        buttonWidth: 250,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });

    $("#txthotels").autocomplete({
        source: function (request, response) {
            response($.map(Get_List(request, 1), function (item) {
                return item;
            }))
        },
        select: function (e, i) {
           
            if (i.item.label != 'Not Found') {
                e.preventDefault();
                if (i.item.val != '-1') {
                    $('#txthotels').val('');
                    $('#txthotels').val(i.item.label.trim());
                }
                else {
                    $('#txthotels').val('');
                }
            }
            else {
                e.preventDefault();
                $('#txthotels').val('');
            }
        },
        minLength: 1
    });

    $("#txthtls_search").autocomplete({
        source: function (request, response) {
            response($.map(Get_List(request, 2), function (item) {
                return item;
            }))
        },
        select: function (e, i) {
            if (i.item.label != 'Not Found') {
                e.preventDefault();
                if (i.item.val != '-1') {
                    $('#txthtls_search').val('');
                    $('#txthtls_search').val(i.item.label.trim());
                }
                else {
                    $('#txthtls_search').val('');
                }
            }
            else {
                e.preventDefault();
                $('#txthtls_search').val('');
            }
        },
        minLength: 1
    });

    $("#txt_comp_sec").autocomplete({
        source: function (request, response) {
            response($.map(Get_List(request, 3), function (item) {
                return item;
            }))
        },
        select: function (e, i) {
            if (i.item.label != 'Not Found') {
                e.preventDefault();
                if (i.item.val != '-1') {
                    $('#txt_comp_sec').val('');
                    $('#txt_comp_sec').val(i.item.label.trim());
                }
                else {
                    $('#txt_comp_sec').val('');
                }
            }
            else {
                e.preventDefault();
                $('#txt_comp_sec').val('');
            }
        },
        minLength: 1
    });
});

function Bind_sec_htls_frm_auto_complete() {
    var data_json = JSON.parse(decodeURIComponent($('#hdn_id_json').val()));
    var htls_name= $('#txthotels').val().trim();
    var htls_add= $('#txthtls_search').val().trim();
    var sup_name= $('#txt_comp_sec').val().trim();
    var returnedData = $.grep(data_json.data.data, function (element, index) {
       debugger;
       return element[3] == ((htls_name == "") ? element[3] : htls_name)
        && element[4] == ((htls_add == "") ? element[4] : htls_add)
        && element[6] == ((sup_name == "") ? element[6] : sup_name)
    });
    setData_htls_detals(returnedData);
}

function Bind_sec_htls_frm_auto_complete_clear() {
    if ($("#txthotels").val().trim() == '') {
        var data_json = JSON.parse(decodeURIComponent($('#hdn_id_json').val()));
        setData_htls_detals(data_json.data.data);
    }
}

function Bind_data_on_page_load() {
    $.ajax({
        url: Bind_Country_name,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#drp_country').empty();
            $('#drp_country').append($('<option></option>').val('0').html('Select option'));
            $(data.country).each(function (index, item) {
                $('#drp_country').append($('<option></option>').val(item.countries__id).html(item.countries__name));
            });

            $('#drp_htls_status').empty();
            $(data.htls_status).each(function (index, item) {
                $('#drp_htls_status').append($('<option></option>').val(item[0]).html(item[1]));
            });

            $(data.compt).each(function (index, item) {
                $('#drpCompt').append($('<option></option>').val(item.id).html(item.name));
            });
            $('#drp_country').multiselect('rebuild');
            $('#drpCompt').multiselect('rebuild');
            $('#drp_htls_status').multiselect('rebuild')
            $('ul.multiselect-container.dropdown-menu').perfectScrollbar();  

        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}

function Bind_city_name_func(country) {
    if ($(country).val() == 0) {
        alert('Please select country !!!');
    }
    else {
        //alert(Bind_city_name);
        var model = {Country_id: $(country).val()}
        $.ajax({
            url: Bind_city_name,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                $('#drp_cities').empty();
                $('#drp_cities').append($('<option></option>').val('0').html('Select City'));
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

function Bind_hotel_name(city) {
    if ($(city).val() == 0) {
        alert('Please select any city  !!!');
    }
    else {
        var city_type = $(city).val();
        var model = {city_id: city_type}
        $.ajax({
            url: Match_unmatch_Bind_hotel_name,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                $('#drp_hotels').empty();
                $(data.hotels).each(function (index, item) {
                    $('#drp_hotels').append($('<option></option>').val(item.id).html(item.HotelName));
                });
                $('#drp_hotels').multiselect('rebuild');
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }
}

function Seach_match_unmatch() {
    var city_type = $('#drp_cities').val();
    var selected_sup_type = $("#drpCompt option:selected");
    var sup_type = "";
    selected_sup_type.each(function () {
        sup_type += $(this).val() + ",";
    });
    sup_type = sup_type.replace(/,\s*$/, "").trim();

    var selected_hotel_type = $("#drp_hotels option:selected");
    var hotel_type = "";
    selected_hotel_type.each(function () {
        hotel_type += $(this).val() + ",";
    });
    hotel_type = hotel_type.replace(/,\s*$/, "").trim();

    var selected_hotel_status = $("#drp_htls_status option:selected");
    var hotel_staus = "";
    selected_hotel_status.each(function () {
        hotel_staus += $(this).val() + ",";
    });
    hotel_staus = hotel_staus.replace(/,\s*$/, "").trim();
    
    var selcountry = $('#drp_country').val();
    var match_nmatch = '';
    if ($('#match').prop('checked')) {
        match_nmatch = match_nmatch + '1,';
    }
    if ($('#unmatch').prop('checked')) {
        match_nmatch = match_nmatch + '2';
    }
    match_nmatch = match_nmatch.replace(/,\s*$/, "").trim();
        if (sup_type == '' )
        {
            alert('Please select atleast one supplier !!!');
            return false;
        }
        if (selcountry == 0 )
        {
            alert('Please select atleast one country !!!');
            return false;
        }
        if (city_type =='0')
        {
            alert('Please select atleast one city !!!');
            return false;
        }
        if (hotel_type =='')
        {
            alert('Please select atleast one hotel !!!');
            return false;
        }

        if (hotel_staus =='')
        {
            alert('Please select hotels status !!!');
            return false;
        }
        

        var model = {
            primry_sup__id: 1,
            city_id: city_type,
            primary_hotel_id: hotel_type,
            secondry_sup_id: sup_type,
            hotel_status_id: hotel_staus,
            matching_status_id: match_nmatch
        };
        var urls= 'https://'+SERVICES_IP+'/api/v1/sample/sp_Bind_grid_for_UI'
        $.ajax({
            url: urls,
            type: 'GET',
            data: model,
            dataType: 'json',
            crossDomain: true,
            success: function (data) {
                debugger;
                setData(data);
                if (data.data.data.length==0)
                {
                    alert('No record found !!!');
                }
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });

    }

function reset_frm()
{
    window.location.href=window.location.href;
}
 
function Get_List(request, req_type) {
    var data_json = JSON.parse(decodeURIComponent($('#hdn_id_json').val()));
    var list = [];
    if (req_type == 1) {
        jQuery(data_json.data.data).each(function (i, item) {
            if (item[3].toUpperCase().trim().indexOf(request.term.toUpperCase().trim()) >= 0) {// for status
                var model = {label: item[3], val: item[0]}
                var added = false;
                $.map(list, function (elementOfArray, indexInArray) {
                    if (elementOfArray.label.toUpperCase().trim() == item[3].toUpperCase().trim()) {
                        added = true;
                    }
                })
                if (!added) {
                    list.push(model);
                }
            }
        });
    }
    else if (req_type == 2) {
        jQuery(data_json.data.data).each(function (i, item) {
            if (item[4].toUpperCase().trim().indexOf(request.term.toUpperCase().trim()) >= 0) {// for status
                var model = {label: item[4], val: item[0]}
                var added = false;
                $.map(list, function (elementOfArray, indexInArray) {
                    if (elementOfArray.label.toUpperCase().trim() == item[4].toUpperCase().trim()) {
                        added = true;
                    }
                })
                if (!added) {
                    list.push(model);
                }
            }
        });
    }


    else if (req_type == 3) {
        jQuery(data_json.data.data).each(function (i, item) {
            if (item[6].toString().toUpperCase().indexOf(request.term.toUpperCase().trim()) >= 0) {// for status
                var model = {label: item[6], val: item[0]}
                var added = false;
                $.map(list, function (elementOfArray, indexInArray) {
                    if (elementOfArray.label.toString().toUpperCase().trim() == item[6].toString().toUpperCase().trim()) {
                        added = true;
                    }
                })
                if (!added) {
                    list.push(model);
                }


            }


        });
    }

    if (list.length == 0) {
        var model_new = {label: 'Not Found', val: '-1'};
        list.push(model_new);
    }
    return list;
}


function reset_frm()
{
    window.location.href =window.location.href ;
}

function setData(data) {
    $('#div_tbl_main_grid').show();
    var table = $("#hotel_match_unmatch").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';

    var sec_htl_link = '';
    var chk_bx = '';
    var read_only = '';
    var is_match = '';
    $.each(data.data.data, function (i, item) {
       debugger;
        if (item[25] != null && item[25].toString().toUpperCase() == 'MATCHED') {
            sec_htl_link = '' + item[20] + ''
            is_match = 'true';
            chk_bx = 'checked';
        }
        else {
            sec_htl_link = '<a  data-toggle="modal" data-target="#myModal"  onclick="Bind_secondry_htls_details(' + item[0] + ');" class="select_hotel_click"> Select hotel </a>'
            chk_bx = '';
            //read_only = '';
            read_only='disabled';
            is_match = 'false';
        }
        trHTML += '<tr id="tr_grid_match_' + item[0] + '">' +
            '                            <td>' + item[9] + '<p style="display:none;" id="hdn_primary_htls_id_main_'+item[0]+'">'+item[8]+'</p></td>' +
            '                            <td>' + item[11] + '</td>' +
            '                            <td><span class="circle green">' + item[26] + '</span></td>' +
            '                            <td><span class="h_address"> ' + item[12] + ' </span></td>' +
            '                            <td>' + item[14] + '</td>' +
            '                            <td>' + item[15] + '</td>' +
            '                            <td><span class="text-uppercase">' + item[19] + '</span></td>' +
            '                            <td> ' + item[17] + '</td>' +
            '                            <td>' + sec_htl_link + '</td>' +
            '                            <td><span class="h_address"> ' + item[21] + ' </span></td>' +
            '                            <td>' + item[22] + '</td>' +
            '                            <td>' + item[23] + '</td>' +
            '                            <td>' + item[25] + '</td>' +
            '                            <td>' + item[24] + '</td>' +
            
 '                                 <td>not calculated</td>' +
 //'                            <td><input id="chk_bx_grid_'+item[0]+'" type="checkbox" checked="checked"> </td>' +
 ' <td>' +
 '                                <label class="switch">' +
 '                                   <input class="switch-input " value="' + is_match + '"  id="chk_bx_grid_' + item[0] + '"    type="checkbox"         onchange="set_flag_formatch_n_unmatch(' + item[0] + ')"   '+chk_bx+'   '+read_only+'/>' +
 '                                    <span class="switch-label" data-on="MATCH" data-off="UNMATCH" ></span>' +
 '                                    <span class="switch-handle"></span>' +
 '                                </label>' +
 '                           </td>'

'                        </tr>';
      

    });
   
    $('#id_tbl_body').append(trHTML);
    $('#hotel_match_unmatch').DataTable({
        "sPaginationType": "full_numbers",
        "bFilter": true,
        "bInfo": false,
        "bPaginate": true,
        scrollX: true,
        scrollCollapse: true,
        paging: true,
        fixedColumns: {
            leftColumns: 0,
            rightColumns: 1
        }

    });
    $('.dataTables_scrollBody').perfectScrollbar();
    // $('#drp_cities').empty();
    // $('#drp_cities').append($('<option></option>').val('0').html('Select option'));
    // $('#drp_country').val('0');
    // $('#drpCompt').val('0');
    $('#div_tbl_main_grid').show();
}

function setData_htls_detals(data) {
   
    var table = $("#selected_hotels_grid").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {
        trHTML += '<tr id="tr_sel_grid_' + item[0] + '" class="row_contaner">' +
            '                                    <td>' +
            '                                        <div class="radio radio-primary">' +
            '                                            <input id="grd_rad_' + item[0] + '" type="radio" name="radio" >' +
            '                                            <label for="grd_rad_' + item[0] + '"></label>' +
            '                                        </div>' +
            '                                    </td>' +
            '                                    <td width="14%">' + item[1] + '<p style="display:none;" id="hdn_secondry_htls_id_In_grid_'+item[0]+'">'+item[2]+'</p></td>' +
            '                                    <td width="14%">' + item[3] + '</td>' +
            '                                    <td width="14%">' + item[4] + '</td>' +
            '                                    <td width="14%">' + item[7] + '</td>' +
            '                                    <td width="14%">' + item[8] + '</td>' +
            '                                    <td width="14%">' + item[9] + '</td>' +
            '                                    <td width="14%">' + item[6] + '</td>' +
            '                                </tr>';


    });
   
    $('#tbody_selec_grid_second').append(trHTML);
    $('#selected_hotels_grid').DataTable({
        "sPaginationType": "full_numbers",
        "bFilter": true,
        "bInfo": false,
        "bPaginate": true,
        scrollX: true,
        scrollCollapse: true,
        paging: true,
    });
    $('.dataTables_scrollBody').perfectScrollbar();
    $('.dataTables_scrollBody,.addhotel_checkbox_contaner').perfectScrollbar();
}

function Save_match_unmatch() {
    var sec_id = '';var row_count =0;
    var table = $('#hotel_match_unmatch').dataTable();
    $(table.fnGetNodes()).each(function (i, item) {
       
        var act_id = item.id.replace('tr_grid_match_', '')
        if (($('#hdn_p_flag_id_' + act_id + '').text().trim() != '' && $('#hdn_p_flag_id_' + act_id + '').text().trim().toString() == 'true') || ($('#hdn_p_sec_id_tr_grid_match_' + act_id + '').text().trim() != '')) {
            var unmatch= '';    var match= ''; var primary_htls_id ='';
           
            row_count=row_count+1;
            if (!$('.DTFC_Cloned #chk_bx_grid_' + act_id + '').prop('checked'))
            {
                unmatch= unmatch+act_id.toString() + ',';
            }
             if ($('.DTFC_Cloned #chk_bx_grid_' + act_id + '').prop('checked'))
            {
                 var prim_id = $('#hdn_primary_htls_id_main_'+act_id).text();
                 primary_htls_id= primary_htls_id+prim_id+',';
                 sec_id = sec_id + $('#hdn_p_sec_id_tr_grid_match_' + act_id + '').text().trim() + ',';
                
            }

            var model = {
            primary_sup__id_unmatch: unmatch.replace(/,\s*$/, "").trim(),
            Sec_sup__id_match: sec_id.replace(/,\s*$/, "").trim(),
            primary_htls_id :primary_htls_id.replace(/,\s*$/, "").trim(),
            Session_id: '1'
        };
        $.ajax({
            url: 'https://'+SERVICES_IP+'/api/v1/sample/sp_update_match_unmatch_frm_UI',
            type: 'GET',
            data: model,
            dataType: 'json',
            crossDomain: true,
            success: function (data) {
                alert('Save successfully ');
                return false;
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });

        }
        
        if (row_count==0)
        {
            alert('There is no match unmatch operation performed in list !!!');
            return false;
        }
         
    });
}

function Bind_secondry_htls_details(rowId) {
   
    rowId = 'tr_grid_match_' + rowId;
    $('#hdn_primary_grid_id').val('');
    $('#hdn_primary_grid_id').val(rowId);
    var city_type = $('#drp_cities').val();
    var selected_sup_type = $("#drpCompt option:selected");
    var sup_type = "";
    selected_sup_type.each(function () {
        sup_type += $(this).val() + ",";
    });
    sup_type = sup_type.replace(/,\s*$/, "").trim();
    if (city_type != '' && sup_type != '') {
        var model = {
            city_id: city_type,
            secondry_sup_id: sup_type,
        };

        $.ajax({
            url: 'https://'+SERVICES_IP+'/api/v1/sample/sp_Bind_grid_for_Sec_popup',
            type: 'GET',
            data: model,
            dataType: 'json',
            crossDomain: true,
            success: function (data) {
                var val_js = encodeURIComponent(JSON.stringify(data)); //setting json in hidden field
                $('#hdn_id_json').val(val_js);
                setData_htls_detals(data.data.data);
            },
            error: function (xhr, errorType, exception) {
                alert(exception);
            }
        });

    }
    else {
        alert('Validation failed !!');
    }

}

function get_sec_htls_details() {
    var rd_chk_count = 0;
    var table = $('#selected_hotels_grid').dataTable();
    $(table.fnGetNodes()).each(function (i, item) {
        var tr = $('#' + item.id + '');
        if (tr.find('input[type=radio]').prop('checked')) {
            rd_chk_count = rd_chk_count + 1;
            var hotel_name = tr.find("td:eq(2)").text();
            var hotel_address = tr.find("td:eq(3)").text();
            var hotel_apper_on = tr.find("td:eq(4)").text();
            var longi = tr.find("td:eq(5)").text();
            var lat = tr.find("td:eq(6)").text();
           
            if ($('#hdn_primary_grid_id').val().trim() != '') {
                var tr_main_grid = $('#' + $('#hdn_primary_grid_id').val().trim() + '');
                tr_main_grid.find("td:eq(8)").text(hotel_name)
                tr_main_grid.find("td:eq(9)").text(hotel_address)
                tr_main_grid.find("td:eq(10)").text(longi)
                tr_main_grid.find("td:eq(11)").text(lat)
                tr_main_grid.find("td:eq(14)").text(hotel_apper_on);
                var act_sec_id = item.id.replace('tr_sel_grid_', '')
                var sec_htls_main_id = $('#hdn_secondry_htls_id_In_grid_'+act_sec_id+'').text();
                tr_main_grid.find("td:eq(4)").html(tr_main_grid.find("td:eq(4)").text() + '<p id="hdn_p_sec_id_' + $('#hdn_primary_grid_id').val().trim() + '" style="display: none">' + act_sec_id + '</p>')
                var Act_main_grid_id = $('#hdn_primary_grid_id').val().trim().replace('tr_grid_match_', '');
                $('.DTFC_Cloned #chk_bx_grid_' + Act_main_grid_id + '').prop('checked', true);
                $(".modal-backdrop.in").hide();
                $("body").removeClass('modal-open');
                $(".modal").slideUp('fast');
                return false;
            }
        }


    });

    if (rd_chk_count == 0) {
        alert('Please select any  secondry hotels !!!');
    }

}

function set_flag_formatch_n_unmatch(id) {
    var tr_main_grid = $('#tr_grid_match_' + id);
    var chk_bx = $('#chk_bx_grid_' + id);
    var old_chk_val = (chk_bx.val());
    var new_chk_val = ($('.DTFC_Cloned #chk_bx_grid_' + id + '').prop('checked'));

    var tr_5_val =tr_main_grid.find("td:eq(5)").text().replace('true','').replace('false','');
    if (old_chk_val.toString() == new_chk_val.toString()) {
       // alert(tr_main_grid.find("td:eq(5)").text()+'<p id="hdn_p_flag_id_' + id + '" style="display: none">false</p>')
        tr_main_grid.find("td:eq(5)").html(tr_5_val + '<p id="hdn_p_flag_id_' + id + '"  style="display: none" >false</p>')
        //tr_5_val='';
    }
    else {
       // alert(tr_main_grid.find("td:eq(5)").text())
        tr_main_grid.find("td:eq(5)").html(tr_5_val + '<p id="hdn_p_flag_id_' + id + '" style="display: none" >true</p>')
        //tr_5_val='';
    }
}


 function download_template () {
    window.location.href ='/static/Excel_Templates/match_unmatch_template.xlsx';
 }

 function Excel_upload_Match_unmatch()
 {
    var file_val = $("#excel_upload_file_control").val();
      if (file_val == '') {
        alert('Please select file and upload !!!');
        return false;
      }
      var fileUpload = $("#excel_upload_file_control").get(0);
      var files = fileUpload.files;
      var formdata = new FormData();
      formdata.append("File", files[0]);
      $.ajax({
        url: matach_unmatch_upload_excel,
        type: "POST",
        processData: false,
        dataType: 'json',
        data: formdata,
        contentType: false,
        success: function (data) {
          $("#excel_upload_file_control").val(null);
          $('.file_type').text('');
          $('.file_type').css('opacity', '0');
          if (data.count > 0) {
            alert('Please  check downloded  Error file !!!');
           // window.location.href = data.Path;
          }
          else {
            alert(data.htl_grp_dtls);
          }
        },
        error: function (xhr, errorType, exception) {
          alert(exception)
        }
      });
 }


