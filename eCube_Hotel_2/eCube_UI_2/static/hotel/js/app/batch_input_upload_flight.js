upload_batch_input_flight = function() {
	var file_val = $("#input_file_excel").val();
    if (file_val == ''){
        alert('Please select file and upload !!!');
        return false;
	}
	
	var fileUpload = $("#input_file_excel").get(0);
    var files = fileUpload.files;
	var formdata = new FormData();
	formdata.append("File", files[0]);
	$.ajax({
		url: HOTEL_BATCH_INPUT_UPLOAD_URL,
		type: "POST",
		processData: false,
		dataType: 'json',
		data: formdata,
		contentType: false,
		success: function (data) {
			debugger;
			$("#input_file_excel").val(null);
            $('.file_type').text('');
			$('.file_type').css('opacity', '0');
			if (data.msg != undefined && data.msg !='')
			{
				alert(data.msg);
				return false;
			}
			if ( data.download_link != undefined && data.download_link != ''){
				alert('Please  click on  Error log  button for download Error file !!!');
                $('#btn_error').show();
                $('#btn_error').attr('href', data.download_link);
				return false;
			}
			alert(REQUEST_TYPE)
		    switch(REQUEST_TYPE){
		        case 'HOTEL':
					//batch_ids = 'excel_upload';
					dictLength = (data.data.h_new_batches).length
					if (dictLength > 1){
						batch_ids = 'excel_upload';
					}
					else{
						batch_ids = data.data.h_new_batches.join('_');
					}
					
		            break;
				case 'HOTELFLIGHT':
				dictLength = (data.data.hf_new_batches).length
					if (dictLength > 1){
						batch_ids = 'excel_upload';
					}
					else{
						batch_ids = data.data.hf_new_batches.join('_');
					}
		            break;
			}
			
			window.location.href = CREATE_REQUEST_URL + batch_ids+'?url='+dictLength; 
			 
			
		},

		error: function (xhr, errorType, exception) {
			alert(exception)
		}
	});
}

$("#batch_selector").change(function(){
    var selected_req_id = this.value;
    window.location.href = CREATE_REQUEST_URL + selected_req_id;
})

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

$( document ).ready(function() {
	
	var me = getUrlVars()["url"];
	if (me == 1)
	{
		$('#start_schedule').show();
		$('.manually_added').hide();
	}
	else if(me != undefined && me !=''){
		$('.manually_added').hide();
		$('#start_schedule').hide();
	} 
});





 