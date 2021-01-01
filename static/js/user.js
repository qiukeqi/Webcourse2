$('#toLogin').click(function(){
	window.location.href="/login";
})

$("#newpassword").keydown(function(event){
	var e = event || window.event;
	
	if(e.keyCode == 13){
		newPassword = $(this).val();
		$(this).val("");
		changePassword(newPassword);
	}
})

function changePassword(newPassword){
	datas = {};
	datas['newPassword'] = newPassword;
	$.ajax({
		url: 'http://localhost:5000/changePassword',
		type: 'POST',
		dataType: 'json',
		headers: {
			"Content-Type": "application/json;charset=utf-8"
		},
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify(datas),
		success: function(data) {},
		error: function(e) {
			console.log(e);
		}
	});
}

$(".card__image").click(function(){
	$('#hidden-input-field').trigger('click');
})

//当从文件选择界面选择了文件的时候
$('#hidden-input-field').change(function(e) {
	console.log("from input field");
	//获取文件相关信息
	data_file = e.currentTarget.files[0];
	var file_name = data_file.name;
	var total_size = data_file.size;
	var loaded = 0;

	var fr = new FileReader();
	fr.readAsArrayBuffer(e.currentTarget.files[0]);
	fr.onload = function() {
		upload_file_ajax(fr);
	}

	fr.onprogress = function(e) {
		loaded += e.loaded;
	}
})

//根据文件名称和任务id上传指定文件
function upload_file_ajax(file_reader) {
	var binary_data = file_reader.result;
	$.ajax({

		url: 'http://localhost:5000/upload_file',

		type: 'POST',

		dataType: 'json',

		headers: {
			"Content-Type": "application/json;charset=utf-8",
		},
		contentType: false,

		processData: false,

		data: binary_data,

		success: function(data) {
			location.reload();
		},
		error: function(e) {
			console.log(e);
		}

	});
}
