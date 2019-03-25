﻿$(document).ready(function ($) {
    Bind_country_name();
    $("#text_input_search_hotel_beach").bind("keyup", function (e) {
        var div_1_menu = $('#holtel_list_beatch').find("label");
        $.each(div_1_menu, function (i, item) {
            var input = $("#text_input_search_hotel_beach").val();
            if (item.innerText.toUpperCase().trim().indexOf(input.toUpperCase().trim()) >= 0) {
                $(item.parentNode.parentNode).show()
            }
            else {
                $(item.parentNode.parentNode).hide()
            }
        });
    })
    $('.multiselect_box').multiselect({
        includeSelectAllOption: true,
        buttonWidth: 250,
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true
    });
});
function Bind_grid_main(data) {
    debugger;
    var table = $("#datavalidation").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {
        var is_active_class = '';
        var is_act_text = '';
        if (item._active == true) {
            is_act_text = 'Active';
            is_active_class = 'green';
        }
        else {
            is_act_text = 'Inactive';
            is_active_class = 'red';
        }
        trHTML += '<tr class="" id="grd_grp_list_' + item.id + '">' +
            '  <td width="15%">' + item.hotelgroup + '</td>' +
            // '  <td width="20%">Beach</td>' +
            '  <td width="15%"><span class="circle ' + is_active_class + '">' + is_act_text + '</span></td>' +
            '  <td width="15%">' + item.detail_count + '</td>' +
            '  <td><span data-backdrop="static"  data-toggle="modal" data-target="#myModal" class="edit_btn"  onclick="chk_grp_name_(' + item.id + ');">Edit</span></td>' +
            '<td><span class="del_btn" onclick="Delete_main_grp_dtls(' + item.id + ')">Delete</span></td>' +
            '</tr>'

    });
    $('#tbl_body_main_grp_list').append(trHTML);
    $('#datavalidation').dataTable({
        "sPaginationType": "full_numbers",
        "bFilter": true,
        "bLengthChange": false,
        "bInfo": false,
        "bPaginate": true,
        paging: true,
    });
    $('.dataTables_wrapper,.addhotel_checkbox_contaner').perfectScrollbar();
    $('.dataTables_filter').addClass('pull-right');
}

function chk_grp_name_(id)
{
    var text =$('#grd_grp_list_'+id+'').find('td:eq(0)').text();
    $('#txt_grp_name').val(text);
    $('#txt_grp_name').attr('readonly','readonly');
    $('#txt_grp_name').attr('disabled','disabled');
    bind_hotel_name_for_update(id);
}

function bind_hotel_name_for_update(edit_id)
{
  var val = edit_id;
  if ((val)>0)
  {
        var model = {id: val}
        $.ajax({
            url: Bind_hotel_name_for_update,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
               
             main_list = [];
             var list = [];
             $(data.hotels).each(function (index, item) {
                 var model = {
                     city: item.cityid__cityname,
                     country: item.cityid__countries__name,
                     htls: item.HotelName,
                     hdn_id: 'Grd_sel_hotels_input_chk_htl_' + item.id,
                     main_id: item.id,
                 }
                 list.push(model);
             });

             if (list.length > 0) {
                $.merge(main_list, list);
                $('#div_id_hide_show').show();
                Set_Data_sel_grid(main_list);
                $('#hdn_id_hdn').val(edit_id);
                $('#btn_addgroupfrmgrid').hide();
                $('#btn_updategroupfrmgrid').show();
            }
            else {
                alert('Please select any hotels');
                $('hdn_id_hdn').val('');
            }

            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
  }
  else{
  alert('Please select any group !!!!');
  }
}

function Delete_main_grp_dtls(id) {
 if (confirm("Are you sure?")) {
     var model={id:id};
       $.ajax({
        url: delete_grp_details,
        type: 'POST',
        data: model,
        dataType: 'json',
        success: function (data) {
            alert('Group deleted successfully ');
            Bind_grid_main(data.htl_grp_dtls);
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
    }
    return false;
}
function Bind_all_grp_details(data) {
    Bind_grid_main(data);
    $(data).each(function (index, item) {
        $('#drp_mul_grp_name').append($('<option></option>').val(item.id).html(item.hotelgroup));
    });
    
    $('#drp_mul_grp_name').multiselect("rebuild");
    $('ul.multiselect-container').perfectScrollbar();
}
function _drp_click_1(id)
{
      ///$($('.multiselect-container')[0]).css('display','block');
//    $($('ul.multiselect-container.dropdown-menu')[id]).toggleClass('active')
}
$(document).mouseup(function (e){

	var container = $($('ul.multiselect-container.dropdown-menu'));
	if (!container.is(e.target) && container.has(e.target).length === 0){
		container.removeClass('active');
	}
}); 
function Select_all_hotel_beatc(val_this) {
    if ($(val_this).prop('checked')) {
        $('#holtel_list_beatch').find("input:checkbox").prop('checked', true);
    }
    else {
        $('#holtel_list_beatch').find("input:checkbox").prop('checked', false);
    }
    calculate_checked_count();
}
function calculate_checked_count() {
    $('#span_total_count_hotel').text($('#holtel_list_beatch').find("input:checkbox:checked").length)
    if($('#holtel_list_beatch').find("input:checkbox:checked").length==  $('#holtel_list_beatch').find("input:checkbox").length)
    { 
        $('#checkbox3').prop('checked', true);
    }
    else{
        $('#checkbox3').prop('checked', false);
    }
}
function Bind_country_name() {
    $.ajax({
        url: Bind_Country_name,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $(data.country).each(function (index, item) {
                $('#drp_country').append($('<option></option>').val(item.countries__id).html(item.countries__name));
            });
            $(data.compt).each(function (index, item) {
                $('#drpCompt').append($('<option></option>').val(item.id).html(item.name));
            });
            Bind_all_grp_details(data.htl_grp_dtls);
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
        var model = {Country_id: $(country).val()}
        $.ajax({
            url: Bind_city_name,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                $('#drp_cities').empty();
                $('#drp_cities').append($('<option></option>').val('0').html('Select option'));
                $(data.City).each(function (index, item) {
                    $('#drp_cities').append($('<option></option>').val(item.id).html(item.cityname));
                });
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
        var model = {city_id: $(city).val()}
        $.ajax({
            url: Match_unmatch_Bind_hotel_name,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                $('#div_append_hotels').empty();
                $(data.hotels).each(function (index, item) {
                    var hotel = ' <div class="col-md-3 col-sm-6"><div class="checkbox checkbox-primary checkItem"><input id="input_chk_htl_' + item.id + '" type="checkbox" onchange="calculate_checked_count()"><label for="input_chk_htl_' + item.id + '"><span>' + item.HotelName + '</span></label></div></div>';
                    $('#div_append_hotels').append(hotel);
                });

            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }
}
var main_list = [];
function save_val_to_grid() {
    if ($('#holtel_list_beatch').find("input:checkbox:checked").length > 0) {
        var city = $('#drp_cities option:selected').text();
        var country = $('#drp_country option:selected').text();
        var hotels = $('#holtel_list_beatch').find("input:checkbox:checked");
        var list = [];
        $(hotels).each(function (index, item) {
            var model = {
                city: city,
                country: country,
                htls: $("label[for='" + $(item).attr('id') + "']").text(),
                hdn_id: 'Grd_sel_hotels_' + $("label[for='" + $(item).attr('id') + "']").attr('for'),
                main_id: ($("label[for='" + $(item).attr('id') + "']").attr('for')).replace('input_chk_htl_', ''),
            }
            list.push(model);
        });

       

        $(list).each(function (index, item) {
           main_list=   $.grep(main_list, function (e) {
                return e.main_id != item.main_id;
             });
         });

        main_list= main_list.reverse();

        $.merge(main_list, list);
        main_list= main_list.reverse();
        if (list.length > 0) {
            $('#div_id_hide_show').show();
            Set_Data_sel_grid(main_list);
        }
        else {
            alert('Please select any hotels');
        }
    }
    else {
        alert('Please select any hotels  after selecting country and city !!!');
    }


}
function Set_Data_sel_grid(data) {
    var table = $("#selected_hotels_grid").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {
        debugger;
        trHTML += '<tr class="row_contaner" id="' + item.hdn_id + '">' +
            '  <td>' + item.country + '</td>' +
            '  <td>' + item.city + '</td>' +
            '  <td>' + item.htls + '</td>' +
          
            '  <td><span class="del_btn" id ="' + item.hdn_id + '_del_btn" onclick="delete_grid_selcted(' + item.main_id + ');">Delete</span></td>' +
            '  </tr>'
    });
    $('#id_tbl_body').append(trHTML);
    $('#selected_hotels_grid').dataTable({
        "sPaginationType": "full_numbers",
        "bFilter": true,
        "bLengthChange": false,
        "bInfo": false,
        "bPaginate": true,
        paging: true,
    });
    $('.dataTables_filter').addClass('pull-right');
    $('#drp_cities').val('0');
    $('#drp_cities').empty();
    $('#drp_cities').append($('<option></option>').val('0').html('Select option'));
    $('#drp_country').val('0');
    $('#div_append_hotels').empty();
    $('#drpCompt').val('0');
    $('#span_total_count_hotel').text('0');
    $('#checkbox3').prop('checked', false);
}
function delete_grid_selcted(id) {

    if (confirm("Are you sure?")) {
       main_list = $.grep(main_list, function (e) {
        return e.main_id != id;
    });
    Set_Data_sel_grid(main_list);
    }
    return false;

}


function Update_hotel_list_func()
{
debugger;
    var grp_name =  $('#txt_grp_name').val();
    var  grp_Id =   $('#hdn_id_hdn').val();
    var list_hotels = '';
    var table_1 = $('#selected_hotels_grid').dataTable();
    $(table_1.fnGetNodes()).each(function (i, item) {
        var htl_id = $(item).attr('id').replace("Grd_sel_hotels_input_chk_htl_", "");
        list_hotels = list_hotels + htl_id + ',';
    });
    list_hotels= list_hotels.replace(/,\s*$/, "")
    var model = {grp_name: grp_name,  grp_Id:grp_Id, list_hotels:list_hotels }
    $.ajax({
        url: Update_hotel_list,
        type: 'POST',
        data: model,
        dataType: 'json',
        success: function (data) {
                    reset();
                    alert(grp_name + ' updated successfully');
                    Bind_grid_main(data.hotels);
                    
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}

function reset()
{
    var table = $("#selected_hotels_grid").dataTable();
                    table.fnClearTable();
                    table.fnDraw();
                    table.fnDestroy();
                    main_list = [];
                    $('#txt_grp_name').val('');
                    $('#div_id_hide_show').hide();
                    $('#hdn_id_hdn').val('');
                    $('#txt_grp_name').attr('readonly',false);
                    $('#txt_grp_name').attr('disabled',false);
                    $('#btn_addgroupfrmgrid').show();
                    $('#btn_updategroupfrmgrid').hide();
}

function Bind_hotel_name_by_sup(sup) {

    if ($(sup).val() == 0) {
        Bind_hotel_name($('#drp_cities'));
    }
    else if ($('#drp_cities').val() == 0) {
        $(sup).val('0');
        alert('Please select any city  !!!');
    }
    else {

        var model = {Sup_id: $(sup).val(), city_id: $('#drp_cities').val()}

        $.ajax({
            url: DBind_hotel_name_by_sup,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                $('#div_append_hotels').empty();
                $(data.hotels).each(function (index, item) {
                    var hotel = ' <div class="col-md-3 col-sm-6"><div class="checkbox checkbox-primary checkItem"><input id="input_chk_htl_' + item.id + '" type="checkbox" onchange="calculate_checked_count()"><label for="input_chk_htl_' + item.id + '"><span>' + item.HotelName + '</span></label></div></div>';
                    $('#div_append_hotels').append(hotel);
                });
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }
}
function grp_add_to_db() {
    var grp_name = $('#txt_grp_name').val().trim();
    if (grp_name == '') {
        alert('Please enter group name !!!')
        return false;
    }
    else {
        var grp_type = $('#div_btn_beach_grp .active').text().trim();
        var tbl = $('#selected_hotels_grid').dataTable();
        //var htl_id_list=[];
        var htl_is = '';
        if (tbl.fnGetData().length == 0) {
            alert('Please select any Hotels from List !!!');
            return false;
        }
        else {
            var table_1 = $('#selected_hotels_grid').dataTable();
            $(table_1.fnGetNodes()).each(function (i, item) {
                var htl_id = $(item).attr('id').replace("Grd_sel_hotels_input_chk_htl_", "");
                htl_is = htl_is + htl_id + ','
                //htl_id_list.push(htl_id);
            });
            var model = {grp_name: grp_name, grp_type: grp_type, list_hotels: htl_is.replace(/,\s*$/, "")};
            $.ajax({
                url: Save_htls_details,
                type: 'POST',
                data: model,
                dataType: 'json',
                success: function (data) {
                   
                    alert(grp_name + ' Added successfully');
                    reset();
                    Bind_grid_main(data.hotels);
                },
                error: function (xhr, errorType, exception) {
                    alert(exception)
                }
            });
        }

    }

}
function Search_htl_grp() {

    debugger;
    var selected_grp_bli = $("#drp_mul_grp_name option:selected");
    var grp_name = "";
    selected_grp_bli.each(function () {
        grp_name += $(this).val() + ",";
    });
    // var selected_grp_type = $("#drp_mul_grp_type option:selected");
    // var grp_type = "";
    // selected_grp_type.each(function () {
    //     grp_type += $(this).val() + ",";
    // });
    // var selected_act_not = $("#drp_mul_status option:selected");
    // var act_not = "";
    // selected_act_not.each(function () {
    //     act_not += $(this).val() + ",";
    // });
    var act_not ='';
    if ($('#active_chk').prop('checked'))
    {
        act_not =act_not+ '1,';
    }
    if ($('#inactive_chk').prop('checked'))
    {
        act_not = act_not +'2,';
    }
    var model = {
        grp_name: grp_name.replace(/,\s*$/, ""),
        act_not: act_not.replace(/,\s*$/, "")
    }
    $.ajax({
        url: Bind_grid_by_search,
        type: 'POST',
        data: model,
        dataType: 'json',
        success: function (data) {
            debugger;
            Bind_grid_main(data.htl_grp_dtls);
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });

}
function Download_excel_templates() {
    window.location.href ='/static/Excel_Templates/Htls_template.xlsx';
}
function File_upload() {
    var file_val=  $("#input_file_excel").val();
    if (file_val=='')
    {
        alert('Please select file and upload !!!');
        return false;
    }
    var fileUpload = $("#input_file_excel").get(0);
    var files = fileUpload.files;
    var formdata = new FormData();
        formdata.append("File", files[0]);
         $.ajax({
            url: File_upload_excel,
            type: "POST",
            processData: false,
            dataType: 'json',
            data: formdata,
            contentType: false,
            success: function (data) {
                debugger;
               if(data.err_msg_file.trim() =='') 
               {
               alert('Excel file Uploaded Sucessfully ');
               Bind_grid_main(data.htl_grp_dtls);
               }
               else{
                   alert(data.err_msg_file.trim());
               }
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
}
function chk_grp_name_alrdy_exists() {
    debugger;
    var grp_name= $('#txt_grp_name').val().trim();
    if (grp_name!='') {
        var model = {grp_name: grp_name}
        $.ajax({
            url: chk_grp_name,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
                if (data.data!='')
                {
                    $('#txt_grp_name').val('');
                    alert(data.data);
                }
            },
            error: function (xhr, errorType, exception) {
                alert(exception)
            }
        });
    }
}