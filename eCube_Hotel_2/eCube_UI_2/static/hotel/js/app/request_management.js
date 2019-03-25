jQuery(document).ready(function ($) {
    //Data table Script

    function edit_request_redirect(id){
        var requestId=id;
        alert(requestId);
        $.ajax({
          url: "{% url 'hotel_request_management_edit_request_router' %}",
          type:'POST',
          data: {
              'req_id':requestId
          },
           success:function(data){
            window.location.href = data.url
                  
  
  
           },
           error:function(error) {
  
               alert('error:'+error);
           }
  
  
          });
      }


    $('#request_mgmt').dataTable({
        "sPaginationType": "full_numbers",
        "bFilter": true,
        "bInfo": false,
        "bPaginate": true,
        "bLengthChange": false,
        "bAutoWidth": false,
        //"sScrollX": "100%",
        //"sScrollXInner": "110%",
        //"bScrollCollapse": true,
        "aaSorting": [],
        "columnDefs": [
            { "type": "html-num", "targets": 1 }
        ]
    });

	//Data table Script
	$('#popup_table').dataTable({
		//"scrollX": true,
		"sPaginationType": "full_numbers",
		"bFilter": false,
		"bInfo": false,
		"bPaginate": true,
		//"bLengthChange": false,
		"bAutoWidth": false,
		"scrollX": true,
	});

	$(document).mouseup(function (e){var container = $(".succes_popup,.error_popup");if (!container.is(e.target) && container.has(e.target).length ===0){container.slideUp()&& $(".box_overlay").hide(); }});


    $('#licomplte').click(function(){

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Completed"
        }).show();

        $(".filter_bodyarea li").removeClass("active_tabs");
        $("#licomplte").addClass("active_tabs");

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Non-Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Running"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "InQue"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "All"
        }).hide();

    });

    $('#linotstarted').click(function(){

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Completed"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Scheduled"
        }).show();

        $(".filter_bodyarea li").removeClass("active_tabs");
        $("#not_started").addClass("active_tabs");

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Non-Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Running"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "InQue"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "All"
        }).hide();

    });

    $('#linotscheduled').click(function(){

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Completed"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Non-Scheduled"
        }).show();

        $(".filter_bodyarea li").removeClass("active_tabs");
        $("#not_scheduled").addClass("active_tabs");

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Running"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "InQue"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "All"
        }).hide();

    });

    $('#lirun').click(function(){

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Completed"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Non-Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Running"
        }).show();

        $(".filter_bodyarea li").removeClass("active_tabs");
        $("#lirun").addClass("active_tabs");

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "InQue"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "All"
        }).hide();

    });

    $('#liqueu').click(function(){

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Completed"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Non-Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Running"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "InQue"
        }).show();

        $(".filter_bodyarea li").removeClass("active_tabs");
        $("#liqueu").addClass("active_tabs");

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "All"
        }).hide();

    });

    $('#liall').click(function(){

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Completed"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Non-Scheduled"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "Running"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "InQue"
        }).hide();

        $('#request_mgmt tbody tr' ).filter(function(){

             return $.trim($(this).find('td').eq(12).find('span').eq(0).text()) === "All"
        }).show();

        $(".filter_bodyarea li").removeClass("active_tabs");
        $("#liall").addClass("active_tabs");

    });

})
