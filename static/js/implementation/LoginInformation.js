var state = $('#state').html();

//判断当前界面登录的state
if(state == 'success'){//成功返回当前界面，尝试用cookie进入主界面
	console.log("success");
	window.location.href="/index";
}else if(state == 'no user'){//输入的用户名不对
	alert("no such user name");
}else if(state == 'wrong pwd'){//输入的密码不对
	alert("wrong password");
}else if(state == 'invalid register name'){//注册的是否发现名字被别人注册过了
	alert("this name have been used");
}else if(state == 'register success'){//注册成功
	alert("success register");
}else if(state == 'no cookie'){//发现没有对应的cookie 什么都不做 等待用户输入用户名和密码
	
}else{//出现未知错误，需要程序员处理
	alert("state");
}

$('#sign-in').click(function(){
	$('#upload-form').attr('action',"/checkValidation");
})

$('#register').click(function(){
	$('#upload-form').attr('action',"/register");
})