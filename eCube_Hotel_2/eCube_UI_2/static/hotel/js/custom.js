$(window).resize(function () {

	var height = $(window).height();
	var wwidth = $(window).width();
	var div_height = $(".new_mapping").height();
	var iframe_height = $(".border_contaner_frame").height();
	$(".sidebar_contaner,.full_height").css('height', (height - 0) + 'px');
	$(".custom_scroll,.border_contaner_frame_popup,.full_height_side").css('height', (height - 65) + 'px');
	$(".content_area").css('height', (height - 100) + 'px');
	$(".custom_modal .modal-content").css('height', (height - 0) + 'px');
	$(".custom_modal .modal-content").css('width', (wwidth - 0) + 'px');

	$(".iframes").css('height', (iframe_height - 0) + 'px');
	//var width = $(".header_bodyarea").width();
	//	//alert(width);
	//	$(".dataTables_wrapper ").css('width', (width - 0) + 'px');
	//
	//Sidebar toggle on window width
	if ($(window).width() > 990) {
		$(".body_contaner").removeClass("Sidebar_close");
		 $(".show_again").addClass("hide_full");
	} else {
		$(".body_contaner").addClass("Sidebar_close");

		 $(".show_again").removeClass("hide_full");
	}

	$('*').perfectScrollbar('update');

}); //resize ends


//scroll
$('.custom_scroll').perfectScrollbar();
$('.content_area').perfectScrollbar();
$('.scroll_table').perfectScrollbar();
$('.item_info').perfectScrollbar();
$('.table_scroller').perfectScrollbar();
$('.scroll_bar,.custom_modal_body,.Upload_CSV').perfectScrollbar();

//document . ready starts
jQuery(document).ready(function ($) {

	// $('.dataTables_length').hide();
    // $('.dataTables_filter').addClass('pull-right');
	//Initialise resize
	$(window).trigger('resize');

	//**************************Eerror msg start******************************/


	$('.error_msg').click(function () {
		$(".box_overlay").removeClass("hidden");
		$(".error_popup").addClass("bounceInDown");
		$(".error_popup").removeClass("bounceOutDown hidden");
	});
	$('.success_msg').click(function () {
		$(".box_overlay").removeClass("hidden");
		$(".succes_popup").addClass("bounceInDown");
		$(".succes_popup").removeClass("bounceOutDown hidden");
	});

	$('.Cancel_btn').click(function () {
		$(".box_overlay").addClass("hidden");
		$(".error_popup").addClass("bounceOutDown");
		$(".error_popup").removeClass("bounceInDown");
	});
	$('.success_btn').click(function () {
		$(".box_overlay").addClass("hidden");
		$(".succes_popup").addClass("bounceOutDown");
		$(".succes_popup").removeClass("bounceInDown");
	});



	//**************************Eerror msg End******************************/
	// Initialise the vertical slider
	//Sidebar toggle ON click
//	$(".toggle_sidebar").click(function () {
//		$(".body_contaner").toggleClass("Sidebar_close");
//		$(".show_again").toggleClass("hide_full");
//	});
//	//hide-show filters
//	$(".hide_trigger").click(function () {
//		$(this).toggleClass("show")
//			//$(this).next(".form-control,.box_contaner_side").toggleClass("hide");
//		$(this).next(".form-control,.box_contaner_side").slideToggle();
//	});

	//Sidebar toggle ON click
	$(".toggle_sidebar").on('click', function () {
		$(".body_contaner").toggleClass("Sidebar_close");
		$(".show_again").toggleClass("hide_full");
	});
	//hide-show filters
	$(".hide_trigger").on('click', function () {
		$(this).toggleClass("show")
			//$(this).next(".form-control,.box_contaner_side").toggleClass("hide");
		$(this).next(".form-control,.box_contaner_side").slideToggle();
	});


	$(".extratext").click(function () {
		//debugger;
		$(this).parent().parent().next(".child_row").toggleClass("show_tr");
	});

	$(".full_screen").click(function () {
		$(".table_contaner").toggleClass("full_screenopen");

	});
	$('.scroll_table').perfectScrollbar();

	//File upload
	$('.upload input').change(function () {

		 var filename = this.value;
		var lastIndex = filename.lastIndexOf("\\");
		if (lastIndex >= 0) {
			filename = filename.substring(lastIndex + 1);
		}
		$(this).siblings(".file_type").text(filename).css("opacity", "1");
	});

	$(".table_scroller").hover(function(){
	 //$('*').perfectScrollbar('update');
	 $('.item_info').perfectScrollbar();
	});

}); //document . ready End

//Datepicker Script Starts
$(function () {
	var dateFormat = "mm/dd/yy",
		from = $(".from")
		.datepicker({
			defaultDate: "+1w",
			changeMonth: true,
			minDate: '0',
			numberOfMonths: 1
		})
		.on("change", function () {
			to.datepicker("option", "minDate", getDate(this));
		}),
		to = $(".to").datepicker({
			defaultDate: "+1w",
			changeMonth: true,
			minDate: '0',
			numberOfMonths: 1
		})
		.on("change", function () {
			from.datepicker("option", "maxDate", getDate(this));
		});

	function getDate(element) {
		var date;
		try {
			date = $.datepicker.parseDate(dateFormat, element.value);
		} catch (error) {
			date = null;
		}

		return date;
	}
});

//Datepicker Script Ends



$(function () {
	$('.tags_3').tagsInput({
		width: 'auto'
	});
});

//Clone and Remove Form Fields
$('#add_row').on('click', function () {
	$('#row_contaner').append('<div class="row marT10  animated fadeIn border_top_small"><div class="col-md-2 col-sm-3 col-xs-11"><label class="hidden-md hidden-lg">From Record No</label> <input type="text" class="form-control small_textbox" placeholder="eg:2"></div><div class="col-md-2 col-sm-3 col-xs-11"><label class="hidden-md hidden-lg">To Record No</label><input type="text" class="form-control small_textbox"placeholder="eg:20"></div><div class="col-md-5 col-sm-5 col-xs-10"><label class="hidden-md hidden-lg">Enter Domain URL</label><input  type="text" class="tags tags_3 form-control" ></div><div class="col-md-2 col-xs-1 remove"> <a href="#" class="add_url"  data-toggle="tooltip" title="Remove Row"><img src="images/tag_remove.png"></a> </div><div class="clearfix"></div></div>');
	$('.tags_3').tagsInput({});
	$('[data-toggle="tooltip"]').tooltip();
	return false; //prevent form submission

});

var timecounterid =1
var weekcounterid = 2
var monthcounterid = 1
$('#div2,#id_contaner2,#time_for_weekly,#time_for_month,.Upload_CSV').on('click', '.remove', function () {
	$(this).parent().remove();
	$('*').perfectScrollbar('update');
	return false; //prevent form submission
});

$('#id_contaner2').on('click', '.remove', function () {
	$(this).parent().remove();
	timecounterid--;
	$('*').perfectScrollbar('update');
	return false; //prevent form submission
});


$('#time_for_weekly').on('click', '.remove', function () {
	$(this).parent().remove();
	weekcounterid--;
	$('*').perfectScrollbar('update');
	return false; //prevent form submission
});


$('#time_for_month').on('click', '.remove', function () {
	$(this).parent().remove();
	monthcounterid--;
	$('*').perfectScrollbar('update');
	return false; //prevent form submission
});



//Clone and------------------------------------
$('.add_crawler').on('click', function () {
    row_no = $(this).data('rowno');

    upload_row = $('.file-upload-row').eq(0).clone();
    file_field = upload_row.find('.fileField').eq(0);
    domain_field = upload_row.find('.domains').eq(0);
    multi_select = upload_row.find('.multipleSelect').eq(0);
    file_field.attr('name', 'upload_files_' + row_no);
    domain_field.attr('name', 'domains_' + row_no);

    $('.Upload_CSV').append(upload_row);
    upload_row.show();
    $('*').perfectScrollbar('update');
    multi_select.fastselect();
    $('[data-toggle="tooltip"]').tooltip();

    row_no = parseInt(row_no) + 1;
    $(this).data('rowno', row_no);
    return false; //prevent form submission

});


function Display_msg_hotel(msg,msg_type)
{
	if (msg_type==1) // for sucess
	{
		$('#p_success_id').html('');
		$('#p_success_id').html(msg);
		$(".box_overlay").removeClass("hidden");
		$(".box_overlay").show();
		$(".succes_popup").addClass("bounceInDown");
		$(".succes_popup").show();
		$(".succes_popup").removeClass("bounceOutDown hidden");
	}
	else {
		$('#p_error_id').html('');
		$('#p_error_id').html(msg);
		$(".box_overlay").removeClass("hidden");
		$(".box_overlay").show();
	 	$(".error_popup").addClass("bounceInDown");
	 	$(".error_popup").show();
	 	$(".error_popup").removeClass("bounceOutDown hidden");
		
	}

}

function setfilename(file)
{
	var filename = file.value;
	var lastIndex = filename.lastIndexOf("\\");
	if (lastIndex >= 0) {
	filename = filename.substring(lastIndex + 1);
	}
	$(file).siblings(".file_type").text(filename).css("opacity", "1");

}

function Display_msg_hotel(msg,msg_type)
{
	if (msg_type==1) // for sucess
	{
		$('#p_success_id').html('');
		$('#p_success_id').html(msg);
		$(".box_overlay").removeClass("hidden");
		$(".box_overlay").show();
		$(".succes_popup").addClass("bounceInDown");
		$(".succes_popup").show();
		$(".succes_popup").removeClass("bounceOutDown hidden");
	}
	else {
		$('#p_error_id').html('');
		$('#p_error_id').html(msg);
		$(".box_overlay").removeClass("hidden");
		$(".box_overlay").show();
	 	$(".error_popup").addClass("bounceInDown");
	 	$(".error_popup").show();
	 	$(".error_popup").removeClass("bounceOutDown hidden");

	}
}



// $('.dataTables_length').hide();
// $('.dataTables_filter').addClass('pull-right');
