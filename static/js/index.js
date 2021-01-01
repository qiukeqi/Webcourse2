var bookTagsBufferOld = new Array();
var bookTagsBufferNew = new Array();
var bookNameBuffer;
var readedpageBuffer;
var totalpageBuffer;
//id标识便于筛选
var count = 0;
// 第一次加载执行
window.onload = function() {
	w_getData();
}

function intersect(a,b){
	let set1 = new Set(a),set2 = new Set(b);
	return [...new Set([...set1].filter( x => set2.has(x)))];
}

function difference(a,b){
	let set1 = new Set(a),set2 = new Set(b);
	return [...new Set([...set1].filter(x => !set2.has(x))),...new Set([...set2].filter(x => !set1.has(x)))];
}

function changeBookName(newname,bid){
	if(bookNameBuffer == undefined || bookNameBuffer == null || bookNameBuffer == newname){
		return;
	}
	
	datas = {};
	datas['newname'] = newname;
	datas['bid'] = bid;
	$.ajax({
		url: 'http://localhost:5000/changeBookName',
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



function mupdate(){
	updateOrigin(window.jQuery);
	$('.book-tags-input').unbind('click');
	$('.book-tags-input').unbind('blur');
	$('.book-name').unbind('dblclick');
	
	function quitNameEditMode(t){
		t.attr('contenteditable','false');
		changeBookName(t.html(),t.parent().attr('listid'));
	}
	
	$('.book-name').dblclick(function(){
		//双击之后将当前name变为可编辑的
		currentState = $(this).attr('contenteditable');
		if(currentState == "true"){
			quitNameEditMode($(this));
		}else{
			bookNameBuffer = $(this).html();
			$(this).attr('contenteditable','true');
			$(this).focus();
			//保存一下当前的book名称
			bookNameBuffer = $(this).html();
		}
	})
	
	$('.book-name').keydown(function(event){
		e = event || window.event;
		if(e.keyCode == 13){//按下enter键退出这个模式
			quitNameEditMode($(this));
		}
	})
	
	$('.book-name').blur(function(event){//失去焦点退出编辑模式
		quitNameEditMode($(this));
	})
	
	$('.book-tags-input').click(function(){
		bookTagsBufferOld.length = 0;
		spans = $(this).parent().children(".tag");
		for(i = 0; i < spans.length; i++){
			bookTagsBufferOld[i] = spans[i].innerText;
		}
	});
	
	$('.book-tags-input').blur(function(){
		bookTagsBufferNew.length = 0;
		spans = $(this).parent().children(".tag");
		for(i = 0; i < spans.length; i++){
			bookTagsBufferNew[i] = spans[i].innerText;
		}
		inter = intersect(bookTagsBufferNew,bookTagsBufferOld);
		added = difference(inter,bookTagsBufferNew);
		deleted = difference(inter,bookTagsBufferOld);
		bid = $(this).parent().parent().parent().attr("listid");
		if(bid == undefined){
			return;
		}
		changeBookTags(added,deleted,bid);
	});
	
	//刷新阅读记录的事件
	$(".readedpage").focus(function(){
		readedpageBuffer = $(this).html();
		console.log("focus");
	})
	$(".readedpage").blur(function(){
		//没有更改就不会发送请求更改数据的请求
		if(readedpageBuffer == undefined || readedpageBuffer== null || readedpageBuffer == $(this).html()){
			return;
		}
		//发送更改数据的请求
		changePage('read',$(this).parent().parent().parent().attr('listid'),$(this).html());
	})
	
	$(".totalpage").focus(function(){
		totalpageBuffer = $(this).html();
	})
	
	$(".totalpage").blur(function(){
		//没有更改就不会发送请求更改数据的请求
		if(totalpageBuffer == undefined || totalpageBuffer== null || totalpageBuffer == $(this).html()){
			return;
		}
		//发送更改数据的请求
		changePage('total',$(this).parent().parent().parent().attr('listid'),$(this).html());
	})
	
	function changePage(type,bid,value){
		datas = {};
		datas['type'] = type;
		datas['bid'] = bid;
		datas['value'] = value;
		$.ajax({
			url: 'http://localhost:5000/changePage',
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
}

function changeBookTags(added,deleted,bid){
	datas = {};
	datas['added'] = added;
	datas['deleted'] = deleted;
	datas['bid'] = bid;
	$.ajax({
		url: 'http://localhost:5000/changeBookTags',
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

function w_getData(keyword = "") {
	//清除之前的数据，防止有重复的数据出现在界面上
	$("#content").html("");
	//以json的形式构建上传给服务器的数据
	datas = {};
	datas['keyword'] = keyword;
	$.ajax({
		url: 'http://localhost:5000/getAll',
		type: 'POST',
		dataType: 'json',
		headers: {
			"Content-Type": "application/json;charset=utf-8"
		},
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify(datas),
		success: function(data) {
			books = data['books'];
			tags = data['tags'];
			//将所有的书都列出来，但是没有为每本书加上tags
			for(i = 0; i < books.length; i++){
				addTemplate(books[i]['name'],books[i]['date'],books[i]['bid'],books[i]['readpage'],books[i]['totalpage']);
			}
			
			//让插件根据现有的book生成布局
			mupdate();
			
			//为每本书添加tags
			var env = $.Event('keydown',{keycode : 13});
			for(i = 0; i < tags.length; i++){
				target = "[listid = " + tags[i]['bid'] + "]";
				div = $(target).find(".book-tags .bootstrap-tagsinput input");
				div.val(tags[i]['tn']);
				div.keypress();
			}
		},
		error: function(e) {
			console.log(e);
		}
	
	});
}

$(function() {
	//添加book信息的点击事件
	$('#add').click(function() {
		// 非空验证
		if ($('#todo').val() == '') {
			return
		}
		rand = Math.random();
		time = w_nowTime();
		var todo = {};
		todo.things = $('#todo').val();
		addBook(todo.things,rand);
		//存储完成后清空输入框
		$('#todo').val('');
		// 更新列表
		addTemplate(todo.things,time,rand,0,200);
		//为tags刷新事件
		mupdate();
	})

	// 触发edit事件
	$(document).on('click', '#edit_tags', function() {
			
		if($(this).parent().next().hasClass("hidden")){
			$(this).parent().next().removeClass("hidden");
			
		}else{
			$(this).parent().next().addClass("hidden");
		}
	})

	//delete删除事件(采用事件委托的方式，方式新增html元素找不到事件)
	$(document).on('click', '#delete', function() {
		bid = $(this).parent().parent().attr('listid');
		datas = {};
		datas['bid'] = bid;
		$.ajax({
			url: 'http://localhost:5000/delete',
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
		
		$(this).parent().parent().remove();
	})
	//时间函数
	function w_nowTime() {
		var myDate = new Date();
		var year = myDate.getFullYear(); //获取完整的年份(4位,1970-????)
		var month = myDate.getMonth() + 1; //获取当前月份(0-11,0代表1月)
		var day = myDate.getDate(); //获取当前日(1-31)
		var week = myDate.getDay(); //获取当前星期X(0-6,0代表星期天)
		var hour = myDate.getHours(); //获取当前小时数(0-23)
		var minutes = myDate.getMinutes(); //获取当前分钟数(0-59)
		var seconds = myDate.getSeconds(); //获取当前秒数(0-59)
		return `${year}-${w_zero(month)}-${w_zero(day)} ${w_zero(hour)}:${w_zero(minutes)}:${w_zero(seconds)}`
	}

	//不够补零
	function w_zero(num) {
		if (num < 10) return "0" + num;
		else return num;
	}
	
	function addBook(book_name,oldBookID){
		datas = {};
		datas['bookName'] = book_name;
		$.ajax({
		
			url: 'http://localhost:5000/addBook',
		
			type: 'POST',
		
			dataType: 'json',

			headers: {
				"Content-Type": "application/json;charset=utf-8"
			},
			
			contentType: 'application/json; charset=utf-8',
			
			data: JSON.stringify(datas),
			
			success: function(data) {
				newBookid = data['newBookid'];
				$("[listid = \""+oldBookID+"\" ]").attr('listid',newBookid);
			},
			error: function(e) {
				console.log(e);
			}
		
		});
	}
})

// enter添加事件
$('#todo').keydown(function(event) {
	var e = event || window.event;
	if (e.keyCode == 13) {
		$('#add').click();
	}
});

//进行logout的处理
$('#logout').click(function(){
	window.location.href="/logout";
})

//进入用户信息界面
$('#user').click(function(){
	window.location.href = "/user";
})

//清除现有的search-tags
$('#tag-clear').click(function(){
	$('#search-tags-container .bootstrap-tagsinput .tag').remove();
})

//根据tag搜索
$('#tag-search').click(function(){
	spans = $('#search-tags-container .bootstrap-tagsinput .tag');
	//如果search为空，就展示所有的Book
	if(spans.length == 0){
		showAllBooks();
		return;
	}
	
	//如果不为空，就执行搜索
	showAllBooks();
	var tags = [];
	for(i = 0; i < spans.length; i++){
		tags[i] = spans[i].innerText;
	}
	firstBook = $("#content .Book").first();
	while(firstBook.length != 0){
		currentTags = firstBook.find(".book-tags .bootstrap-tagsinput .tag");
		currentATags = new Array();
		isValid = false;
		for(i = 0; i < currentTags.length; i++){
			isValid = isValid | tags.includes(currentTags[i].innerText);
		}
		
		if(isValid){
			firstBook.removeClass('hidden');
		}else{
			firstBook.addClass('hidden');
		}
		
		firstBook = firstBook.next();
	}
	//console.log($("#content .Book .book-tags .bootstrap-tagsinput .tag"));
})

//function 展示所有的Book
function showAllBooks(){
	$("#content .Book").removeClass('hidden');
}

function addTemplate(bookName,date,id,readpage,totalpage){
	$('#content').append(
		`<div class="Book row" style="" listid="${id}">
			<div class="book-name col-xs-5 col-md-5">${bookName}</div>
	
			<div class="col-md-4 visible-md-block visible-lg-block">
				${date}
			</div>
	
			<div class="col-xs-7 col-md-3">
				<button class="col-xs-6" id="edit_tags">More</button>
				<button class="col-xs-6" id="delete">Delete</button>
			</div>
	
			<div class="col-xs-12 hidden book-tags" style="margin-top: 1rem;">
				<input style="width: 100%;" type="text" data-role="tagsinput" placeholder="tags">
				<div class="read-process">
					<p>read process </p>
					<p class="readedpage" contenteditable="true">${readpage}</p>
					<p>/</p>
					<p class="totalpage" contenteditable="true">${totalpage}</p>
				</div>
			</div>
	
		</div>`
	);
}

$("#submit").unbind('click');


$("#submit").click(function(e){
	w_getData($("#submit-text").val());
	return false;
})

$('#delete').click(function(){
	
})
