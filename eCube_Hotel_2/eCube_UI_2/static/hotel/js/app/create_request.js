$('.close').on('click', function () {
    if ($('.pos_list li').length > 1) {
        $(this).parent("a").parent("li").remove();
    } else {
        $(this).parent("a").parent("li").remove('');
    }
});

$('.collpas_expand').click(function () {
    $(this).toggleClass("opened");
    $(this).siblings(".pos_body").slideToggle();
});


$('.actionable_btn_edit').click(function () {


})


function edit_func(sub_request_id) {
    fill_request_form(sub_request_id);
}

function hotelDetails(REQUEST_ID) {
    if (REQUEST_ID == 'excel_upload') {

    }
    else {
        $.ajax({
            url: hotel_all_bind_hotels,
            type: 'POST',
            data: { "reqt_Id": REQUEST_ID },
            success: function (data) {

                if (data.Hotels != '') {

                    list_hotels = []
                    $.each(data.Hotels, function (key, val) {
                        list_hotels.push(key);
                    });

                    $("#drpHotel").val(list_hotels);
                    $("#drpHotel").multiselect('rebuild')
                }
                else {
                    $(".hotel_selection").hide();
                }

            },
            error: function (x, xhr, type) {
                console.log(type)

            }
        })
    }
}



jQuery(document).ready(function () {
    if (REQUEST_ID != "") {
        $.each(sub_request_json, function (key, value) {

            req = key;
            setTimeout(function () {
                // $('#edit_a_' + req).click();
                edit_func(req)
                $("#batch_key").val(req);
            }, 1001);
            $('#txtRequestName').attr('readonly', true);
            $('#txtRequestDesc').attr('readonly', true);
            setTimeout(function () {
                hotelDetails(REQUEST_ID);
            }, 2001);
            setTimeout(function () {
                $('#hdn_hotel_req_id').val('');
            }, 3001);
            return false;
        });
    }
    else { }
});


function delet_func(sub_request_id) {
    if (confirm("Do You Want to Delete the Record!")) {
        $.ajax({
            url: $('#hdn_url2').val(),
            type: 'POST',
            data: { "deletereqId": sub_request_id },
            success: function (data) {
                alert("Successfully Deleted Record")
                var delete_id = data.delete_id
                window.location.href = $('#hdn_url1').val() + data.delete_id
            },
            error: function (x, xhr, type) {
                alert(type)

            }
        })
    }
}

function delet_req_func(request_id) {
    if (confirm("Do You Want to Delete All Record!")) {
        $.ajax({
            url: $('#hdn_url3').val(),
            type: 'POST',
            data: { "deletereqId": request_id },
            success: function (data) {
                alert("Successfully Deleted Record")
                var delete_id = data.delete_id
                window.location.href = $('#hdn_url1').val() + data.delete_id
            },
            error: function (x, xhr, type) {
                alert(type)

            }
        })
    }
}

make_list = function (list_string, sep) {
    if (typeof (list_string) == 'undefined' || !list_string) { }
    else {
        var list_string_list = list_string.split(sep);
        for (i in list_string_list) {
            list_string_list[i] = $.trim(list_string_list[i]);
            //        list_string_list[i] = parseInt(list_string_list[i]);
        }
        return list_string_list
    }
}

make_list_csv = function (list_string) {
    return make_list(list_string, ',')
}

make_list_underscore = function (list_string) {
    return make_list(list_string, '__')
}

read_from_json = function (json_data, key) {

    var ks = make_list_underscore(key);
    var data = json_data;
    for (i in ks) {
        data = data[ks[i]];
    }
    return data
}


input_val = function (input_obj, view_value) {
    var view_value = $.trim(view_value);
    input_obj.val(view_value);
}

multi_select_val = function (input_obj, view_value) {
    if (typeof (view_value) == 'undefined') { }
    else {
        var view_value_list = make_list_csv(view_value);
        input_obj.val(view_value_list);
        input_obj.multiselect("refresh");
    }
}

select_val = function (input_obj, view_value) {
    input_val(input_obj, view_value);
}

select_val_update_children = function (input_obj, view_value) {
    input_val(input_obj, view_value);
    input_obj.trigger('change');
}

select_val_wait_parent = function (input_obj, view_value) {
    setTimeout(function () {
        input_val(input_obj, view_value);
        input_obj.trigger('change');
    }, 1000);
}

multi_select_val_wait_parent = function (input_obj, view_value) {

    setTimeout(function () {
        multi_select_val(input_obj, view_value);
        input_obj.trigger('change');
    }, 2000);
}

weekdays = function (input_obj, view_value) {
    var view_value_list = make_list_csv(view_value);
    var no_of_nights_divs = input_obj.children('.days_btn');

    for (i in no_of_nights_divs) {
        var non = no_of_nights_divs.eq(i);
        non.removeClass('active_day');
    }
    var non = no_of_nights_divs.eq(0);
    if (typeof (view_value_list) == 'undefined') { }
    else {
        for (var i = 0; i < view_value_list.length; i++) {
            $(non.prevObject).each(function (index, value) {
                if (value.innerHTML.toString().trim() === view_value_list[i].toString().trim()) {
                    $(value).addClass('active_day')
                }
            })
        }
    }
}

start_date = function (input_obj, view_value) {

    var view_value_list = make_list_csv(view_value);

    for (var i = 0; i < view_value_list.length; i++) {
        $('#gnBtndate').val(view_value_list[i]);
        $('#btndate').click();

        if (!(i == view_value_list.length - 1)) {
            $('#btndate').click();
        }
    }
    $('#gnBtndate').val('');

}

select_tab = function (input_obj, view_value) {
    selected_tab = view_value;
    switch (selected_tab) {
        case 1:
            $('#ls_daterangedays').click();
            break;
        case 2:
            $('#ls_advancedays').click();
            break;
        case 3:
            $('#ls_checkindays').click();
            break;
        case 4:
            $('#ls_advanceweekdays').click();
            break;
    };
}

advance_days = function (input_obj, view_value) {

    var view_value_list = make_list_csv(view_value);

    var advance_days_divs = input_obj.children('.days_btn');
    for (i in advance_days_divs) {
        var ads = advance_days_divs.eq(i);
        ads.removeClass('active_day');
    }

    for (var i = 0; i < view_value_list.length; i++) {
        adv_days_map = [1, 3, 7, 14];
        default_div = false;
        for (var j = 0; j < 4; j++) {
            if (parseInt(view_value_list[i]) == adv_days_map[j]) {
                default_div = true;
                break;
            }
        }
        if (default_div) {
            for (var k = 0; k < advance_days_divs.length; k++) {
                if (parseInt($(advance_days_divs[k]).text()) == parseInt(view_value_list[i])) {
                    $(advance_days_divs[k]).addClass('active_day');
                    $(advance_days_divs[k]).addClass('active_day days_btn');
                }
            }
        } else {
            $(input_obj).find('.clickable_action append_div').css('style', 'display:inline-block');

            $('#add_advance_days').click();
            $('#gnBtndays').val(view_value_list[i]);
            $('#gnBtndays').focusout();
        }
    }
}

advance_weeks = function (input_obj, view_value) {

    var view_value_list = make_list_csv(view_value);

    var advance_days_divs = input_obj.children('.days_btn');
    for (i in advance_days_divs) {
        var ads = advance_days_divs.eq(i);
        ads.removeClass('active_day');
    }

    for (var i = 0; i < view_value_list.length; i++) {
        if (parseInt(view_value_list[i]) <= 4) {
            for (var k = 0; k < advance_days_divs.length; k++) {
                if (parseInt($(advance_days_divs[k]).text()) == parseInt(view_value_list[i])) {
                    $(advance_days_divs[k]).addClass('active_day');
                    $(advance_days_divs[k]).addClass('active_day days_btn');
                }
            }
        } else {
            $(input_obj).find('.clickable_action append_div').css('style', 'display:inline-block');

            $('#add_advance_days1').click();
            $('#gnBtnAdWeeks').val(view_value_list[i]);
            $('#add_advance_days1').click();
        }
    }
}

no_of_nights = function (input_obj, view_value) {

    var view_value_list = make_list_csv(view_value);

    var no_of_nights_divs = input_obj.children('.count_days');
    for (i in no_of_nights_divs) {
        var non = no_of_nights_divs.eq(i);
        non.removeClass('count_days_selected');
    }

    for (var i = 0; i < view_value_list.length; i++) {
        if (parseInt(view_value_list[i]) <= 6) {
            for (var k = 0; k < no_of_nights_divs.length; k++) {
                if (parseInt($(no_of_nights_divs[k]).text()) == parseInt(view_value_list[i])) {
                    $(no_of_nights_divs[k]).addClass('count_days_selected');
                    $(no_of_nights_divs[k]).addClass('count_days_selected count_days');
                }
            }
        } else {
            $(input_obj).find('.clickable_action append_div').css('style', 'display:inline-block');
            switch (selected_tab) {
                case 1:
                    if (input_obj.selector == '#divrowDateRange') {
                        $('#add_nof').click();
                        $('#gnBtn').val(view_value_list[i]);
                        $('#gnBtn').focusout();
                    }
                    break;
                case 2:
                    if (input_obj.selector == '#divrowDateRange1') {
                        $('#add_nof1').click();
                        $('#gnBtn1').val(view_value_list[i]);
                        $('#gnBtn1').focusout();
                    }
                    break;
                case 3:

                    if (input_obj.selector == '#divstartnights') {
                        $('#add_nof2').click();
                        $('#gnBtn2').val(view_value_list[i]);
                        $('#gnBtn2').focusout();
                    }
                    break;
                case 4:
                    if (input_obj.selector == '#divAdvanceWeekNights') {
                        $('#add_nof3').click();
                        $('#gnBtn3').val(view_value_list[i]);
                        $('#gnBtn3').focusout();
                    }
                    break;
            };
        }
    }
}

crawl_mode = function (input_obj, view_value) {
    var crawl_mode_as = input_obj.children('a');
    for (i in crawl_mode_as) {
        var cm = crawl_mode_as.eq(i);
        cm.removeClass('count_days_selected');
    }

    setTimeout(function () {
        for (i in crawl_mode_as) {
            var cm = crawl_mode_as.eq(i);
            if (parseInt(view_value) == parseInt(cm.data('crawl_mode'))) {
                //cm.addClass('count_days_selected');
                $('.all_hotel').trigger('click');
            }
        }
    }, 2000);

}

fill_input = function (view_value, mapper) {
    if (typeof (view_value) == 'undefined' || !(view_value)) { }
    else {
        var input_obj = $('#' + mapper['input']);

        if (mapper['bind_func']) {
            mapper['bind_func'](input_obj, view_value);
        } else {
            input_val(input_obj, view_value);
        }
    }
}

booking_period_func = function (booking_val) {
    var booking_val = booking_val
    if (booking_val == 1) {
        $("#ls_daterangedays").addClass('icons date_range_icon active')
        $("#date_range").addClass('active in')
        $("#ls_advancedays").addClass('disabled');
        $("#ls_advancedays").removeClass('active');
        $("#advance_days").removeClass('active in');
        $("#ls_checkindays").removeClass('active');
        $("#ls_checkindays").addClass('disabled');
        $("#check_in").removeClass('active in')
        $("#ls_advanceweekdays").addClass('disabled');
        $("#advance_weeks").removeClass('active in')
    }
    else if (booking_val == 2) {
        $("#ls_advancedays").addClass('icons advance_days_icon active')
        $("#advance_days").addClass('active in');
        $("#ls_daterangedays").removeClass('active');
        $("#ls_daterangedays").addClass('disabled');
        $("#date_range").removeClass('active in')
        $("#ls_checkindays").addClass('disabled');
        $("#ls_checkindays").removeClass('active');
        $("#check_in").removeClass('active in')
        $("#ls_advanceweekdays").addClass('disabled');
        $("#advance_weeks").removeClass('active in')

    }
    else if (booking_val == 3) {
        $("#ls_checkindays").addClass('icons check_in_icon active')
        $("#check_in").addClass('active in');
        $("#ls_daterangedays").removeClass('active');
        $("#ls_daterangedays").addClass('disabled');
        $("#date_range").removeClass('active in')
        $("#ls_advancedays").addClass('disabled');
        $("#ls_advancedays").removeClass('active');
        $("#advance_days").removeClass('active in')
        $("#ls_advanceweekdays").addClass('disabled');
        $("#advance_weeks").removeClass('active in')
    }
    else if (booking_val == 4) {
        $("#ls_advanceweekdays").addClass('icons advance_weeks_icon active')
        $("#advance_weeks").addClass('active in');
        $("#ls_daterangedays").removeClass('active');
        $("#ls_daterangedays").addClass('disabled');
        $("#date_range").removeClass('active in')
        $("#ls_checkindays").addClass('disabled');
        $("#check_in").removeClass('active in')
        $("#ls_advancedays").addClass('disabled');
        $("#advance_days").removeClass('active in')
    }

}

fill_request_form = function (sub_request_id) {
    var view_input_mapper = [
        { 'type': 'json', 'input': 'txtRequestName', 'key': 'hotel_request__request_title' },
        { 'type': 'json', 'input': 'txtRequestDesc', 'key': 'hotel_request__request_desc' },

        { 'type': 'json', 'input': 'txtAdultCount', 'key': 'booking__adult_count' },
        { 'type': 'json', 'input': 'txtChildrenCount', 'key': 'booking__children_count' },

        { 'type': 'json', 'input': 'drppointofsale', 'key': 'booking__pos' },

        //Section 2
        { 'type': 'json', 'input': 'drpCountries', 'key': 'booking__country', 'bind_func': select_val_update_children },
        { 'type': 'json', 'input': 'drpCities', 'key': 'booking__city', 'bind_func': select_val_wait_parent },
        { 'type': 'json', 'input': 'drpHotel', 'key': 'booking__hotel', 'bind_func': multi_select_val_wait_parent },

        { 'type': 'html', 'input': 'drpRoomType', 'view': 'board_type_view__sub_request_id_', 'bind_func': multi_select_val },
        { 'type': 'html', 'input': 'drpBoardType', 'view': 'room_type_view__sub_request_id_', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'drpStarRating', 'key': 'booking__star_rating', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'drpBoardType', 'key': 'booking__board_type', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'drpRoomType', 'key': 'booking__room_type', 'bind_func': multi_select_val },

        // Tabs Being
        { 'type': 'json', 'input': 'tab_selector', 'key': 'booking__bookingperiods', 'bind_func': select_tab },
        { 'type': 'json', 'input': 'drpsuppliers', 'key': 'booking__suppliers', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'drpsuppliers1', 'key': 'booking__suppliers', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'drpsuppliers2', 'key': 'booking__suppliers', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'drpsuppliers3', 'key': 'booking__suppliers', 'bind_func': multi_select_val },

        //Section 3
        //{ 'type': 'json', 'input': 'drpsuppliers', 'key': 'booking__suppliers', 'bind_func': multi_select_val },
        { 'type': 'json', 'input': 'txtDateRangeFrom', 'key': 'booking__fromdate' },
        { 'type': 'json', 'input': 'txtDateRangeTo', 'key': 'booking__todate' },

        //Section 4
        { 'type': 'json', 'input': 'divWeekDays', 'key': 'booking__week_days', 'bind_func': weekdays },
        { 'type': 'json', 'input': 'divWeekDays1', 'key': 'booking__week_days', 'bind_func': weekdays },

        { 'type': 'json', 'input': 'divrowDateRange', 'key': 'booking__no_of_nights', 'bind_func': no_of_nights },
        { 'type': 'json', 'input': 'divrowDateRange1', 'key': 'booking__no_of_nights', 'bind_func': no_of_nights },
        { 'type': 'json', 'input': 'divstartnights', 'key': 'booking__no_of_nights', 'bind_func': no_of_nights },
        { 'type': 'json', 'input': 'divAdvanceWeekNights', 'key': 'booking__no_of_nights', 'bind_func': no_of_nights },

        { 'type': 'json', 'input': 'divAdvanceDays', 'key': 'booking__advance_dates', 'bind_func': advance_days },
        { 'type': 'json', 'input': 'divAdvanceWeeks', 'key': 'booking__advance_dates', 'bind_func': advance_weeks },

        { 'type': 'json', 'input': 'divStartDate', 'key': 'booking__advance_dates', 'bind_func': start_date },

        { 'type': 'json', 'input': 'txtName', 'key': 'booking__id' },
        { 'type': 'json', 'input': 'txtName1', 'key': 'booking__batch_id' },

        { 'type': 'json', 'input': 'drpCon1', 'key': 'crawl__mode' },


    ]

    for (i in view_input_mapper) {
        var mapper = view_input_mapper[i];
        switch (mapper['type']) {
            case 'html':
                var view_value = $('#' + mapper['view'] + sub_request_id).html();
                break;
            case 'json':
                var view_value = read_from_json(sub_request_json[sub_request_id], mapper['key']);
                break;
        }
        // console.log(view_value,mapper['key'],"#######################")
        var a = mapper['key'];
        if (a == 'booking__bookingperiods') {
            booking_val = read_from_json(sub_request_json[sub_request_id], mapper['key'])
            booking_period_func(booking_val)
            fill_input(view_value, mapper);

        }
        else if (a == 'booking__id') {
            req_id = read_from_json(sub_request_json[sub_request_id], mapper['key'])
            $('#hdn_edit_id').val('');
            $('#hdn_hotel_req_id').val(req_id);
            fill_input(view_value, mapper);

        }

        else if (a == 'booking__batch_id') {
            req_id = read_from_json(sub_request_json[sub_request_id], mapper['key'])

            $('#batch_selector').val(req_id);



        }

        else if (a == 'booking__hotel') {
            hotelCount = read_from_json(sub_request_json[sub_request_id], mapper['key'])
            if (hotelCount == null || hotelCount == '' || typeof (hotelCount) == 'undefined') {

                setTimeout(function () {
                    $('#AllHotel').click();
                }, 2001);
            }

            else {
                $('#AllHotel').removeClass('active');
                $("#SpecificHotel").addClass('active');
                $("#SpecificHotel").click();

            }
            fill_input(view_value, mapper);

        }

        else if (a == 'booking__room_type') {


            room_type = read_from_json(sub_request_json[sub_request_id], mapper['key'])
            setTimeout(function () {
                if (room_type != null && room_type != '') {
                    Edit_Room_type(room_type);
                }
            }, 3001);
            fill_input(view_value, mapper);
        }

        else {
            fill_input(view_value, mapper);
            $("#drpExcel").hide();
            $("#drpAddMan").hide();
            // $("#gnBtn").hide();
            // $("#gnBtn2").hide();
            $("#gnBtndays").hide();
        }
    }
}

