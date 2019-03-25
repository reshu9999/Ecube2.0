

function uploadbatchinput() {
	alert('test1')
	$.ajax({
		url: 'batchinputupload',		
		type: 'POST',
		dataType: 'json',
		success: function (data) {
			
			alert('OK')
		},
		error: function (xhr, errorType, exception) {
			alert('Fail')
			alert(exception)
		}
	});
	
}




 