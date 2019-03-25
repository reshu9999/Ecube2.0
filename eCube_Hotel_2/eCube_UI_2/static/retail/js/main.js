
$(window).resize(function () {
	var height = $(window).height();
	if ($(window).width() < 990) {
		$(".custom_height").css('height', (height - 150) + 'px');
		$(".custom_height_slideone").css('height', (height - 260) + 'px');
	} else {
		$(".custom_height").css('height', 'auto');
		$(".custom_height_slideone").css('height', 'auto');
	}
	$(".sidebar_contaner").css('height', (height - 0) + 'px');
	$(".custom_scroll").css('height', (height - 62) + 'px');
});

jQuery(document).ready(function ($) {
	$(window).trigger('resize');
	// Initialise the vertical slider
	verticalSlider.init();
	// Initialise Tooltip
	$('[data-toggle="tooltip"]').tooltip();
	//scroll
	$('.custom_scroll').perfectScrollbar();
	//Initialise resize
	
	
});






//second_slide
