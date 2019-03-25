$(document).ready(function ($) {
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
});

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
            $('#drp_man_grp_type').empty();
            $('#drp_man_grp_type').append($('<option></option>').val('0').html('Select option'));
            $(data.Field_master).each(function (index, item) {
                $('#drp_man_grp_type').append($('<option></option>').val(item.id).html(item.name));
            });
            
            Bind_all_grp_details(data.htl_grp_dtls);
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}
function Bind_all_grp_details(data) {
   
    $(data).each(function (index, item) {
        $('#drp_mul_grp_name').append($('<option></option>').val(item.id).html(item.hotelgroup));
    });
    getSelect_hotel();
   
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
function bind_hotel_name_for_update()
{
  var val = $('#drp_mul_grp_name').val();
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
                bind_htls_name_by_group(data.hotels);

            }
            else {
                alert('Please select any hotels');
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
function bind_htls_name_by_group(data)
{
    $('#drp_htls_by_grp').empty();
    $(data).each(function (index, item) {
        $('#drp_htls_by_grp').append($('<option></option>').val(item.id).html(item.HotelName));
    });
    $('#drp_htls_by_grp').multiselect("rebuild");
    $('ul.multiselect-container').perfectScrollbar();
}
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
function delete_grid_selcted(id) {

    if (confirm("Are you sure?")) {
       main_list = $.grep(main_list, function (e) {
        return e.main_id != id;
    });
    Set_Data_sel_grid(main_list);
    }
    return false;

}
function Set_Data_sel_grid(data) {
    var table = $("#selected_hotels_grid").dataTable();
    table.fnClearTable();
    table.fnDraw();
    table.fnDestroy();
    var trHTML = '';
    $.each(data, function (i, item) {
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
        "bInfo": false,
        "bPaginate": true,
        paging: true,
    });

    $('#drp_cities').val('0');
    $('#drp_cities').empty();
    $('#drp_cities').append($('<option></option>').val('0').html('Select option'));
    $('#drp_country').val('0');
    $('#div_append_hotels').empty();
    $('#drpCompt').val('0');
    $('#span_total_count_hotel').text('0');
    $('#checkbox3').prop('checked', false);
}
function chk_grp_name()
{
  var val = $('#drp_mul_grp_name').val();
  if ((val)>0)
  {
    var text =$("#drp_mul_grp_name option:selected").text();
    $('#txt_grp_name').val(text);
    $('#txt_grp_name').attr('readonly','readonly');
    $('#txt_grp_name').attr('disabled','disabled');
    bind_hotel_name_for_update();
        
  }
  else{
  alert('Please select any group !!!!');
  }
}
function Update_hotel_list_func()
{
debugger;
    var grp_name =  $('#txt_grp_name').val();
    var  grp_Id =   $('#drp_mul_grp_name').val();
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
                    var table = $("#selected_hotels_grid").dataTable();
                    table.fnClearTable();
                    table.fnDraw();
                    table.fnDestroy();
                    main_list = [];
                    alert(grp_name + ' updated successfully');
                    $('#txt_grp_name').val('');
                    $('#div_id_hide_show').hide();
                    getSelect_hotel();
        },
        error: function (xhr, errorType, exception) {
            alert(exception)
        }
    });
}
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
function getSelect_hotel()
{
var val = $('#drp_mul_grp_name').val();
  if ((val)>0)
  {
        var model = {id: val}
        $.ajax({
            url: Bind_hotel_name_for_update,
            type: 'POST',
            data: model,
            dataType: 'json',
            success: function (data) {
               
                bind_htls_name_by_group(data.hotels);
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