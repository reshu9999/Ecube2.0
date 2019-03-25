upload_batch_input = function() {
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
		    alert(REQUEST_TYPE)
		    switch(REQUEST_TYPE){
		        case 'HOTEL':
		            batch_ids = data.data.h_new_batches.join('_');
		            break;
		        case 'HOTELFLIGHT':
		            batch_ids = data.data.hf_new_batches.join('_');
		            break;
		    }
            window.location.href = CREATE_REQUEST_URL + batch_ids;
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




 