var deviceWidth = document.documentElement.clientWidth;
//if(deviceWidth > 750) {deviceWidth = 750;}
//document.documentElement.style.fontSize = deviceWidth / 7.5 + 'px';

var ajaxTimeOut = 20000; //ajax超时
var imageMaxSize = 2 * 1024 * 1000;

function hideHeader() {
	if(mui('header').length > 0) {
		mui('header')[0].style.display = 'none';
		mui('body')[0].style.top = '-44px';
	}
	if(document.getElementById('footerMenu')) {
		document.getElementById('footerMenu').style.display = 'none';
	}
}
//不在app内打开链接时，追加header，避免app内header出现忽然消失的效果
function createHeader() {
	if(document.getElementsByTagName("header").length == 0) {
		var title = document.getElementsByTagName("title")[0].text;
		var body = document.getElementsByTagName("body")[0];
		var mui_content = document.getElementsByClassName("mui-content")[0];
		var header = document.createElement("header");
		header.className = "mui-bar mui-bar-nav";
		header.innerHTML = '<a class="mui-action-back mui-icon mui-icon-left-nav mui-pull-left"></a>' +
			'<h1 class="mui-title">' + title + '</h1>'
		body.insertBefore(header, mui_content);
	}
}

//方法同上，带分享图标
function createHeaderWithShare() {
	if(document.getElementsByTagName("header").length == 0) {
		var title = document.getElementsByTagName("title")[0].text;
		var body = document.getElementsByTagName("body")[0];
		var mui_content = document.getElementsByClassName("mui-content")[0];
		var header = document.createElement("header");
		header.className = "mui-bar mui-bar-nav";
		header.innerHTML = '<a class="mui-action-back mui-icon mui-icon-left-nav mui-pull-left"></a>' +
			'<h1 class="mui-title">' + title + '</h1>' +
			'<img id="tagShare" src="../../images/common/fenxiang@3x.png" class="header-fenxiang"/>'
		body.insertBefore(header, mui_content);
	}

}
//有确定的header
function createHeaderWithSure() {
	if(document.getElementsByTagName("header").length == 0) {
		var title = document.getElementsByTagName("title")[0].text;
		var body = document.getElementsByTagName("body")[0];
		var mui_content = document.getElementsByClassName("mui-content")[0];
		var header = document.createElement("header");
		header.className = "mui-bar mui-bar-nav";
		header.innerHTML = '<a class="mui-action-back mui-icon mui-icon-left-nav mui-pull-left"></a>' +
			'<h1 class="mui-title">' + title + '</h1>' +
			'<span class="header-sure"/>确定</span>'
		body.insertBefore(header, mui_content);
	}
}
//获取原生的user_id
function getNativeUserId(userId) {
	if(client == "app") {
		localStorage.setItem("user_id", userId);
	}
}
//登录
function nativeLogin() {
	if(client == "app") {
		document.location = "js://nativeLogin?params=jstojava";
		window.webkit.messageHandlers.nativeLogin.postMessage("123");
	}
}
//返回  共通方法
function pageBack() {
	if(client == "app") {
		document.location = "js://back?params=jstojava";
		window.webkit.messageHandlers.back.postMessage("123");
	}
}
//返回  共通方法
function pageBackReload(param) {
	var str = param || '123';
	if(client == "app") {
		document.location = "js://backReload?params=jstojava";
		window.webkit.messageHandlers.backReload.postMessage(str);
	}
}
//打电话
function callPhone(phone) {
	if(client == 'app') {
		document.location = "js://callPhone?params=" + phone;
		window.webkit.messageHandlers.callPhone.postMessage(phone);
	}
}
//交互方法-调用地图
function callMap(longitude, latitude) {
	if(client == 'app') {
		document.location = "js://callMap?longitude=" + longitude + "&latitude=" + latitude;
		window.webkit.messageHandlers.callMap.postMessage({
			"longitude": longitude,
			"latitude": latitude
		});
	}
}
//交互方法-查询物流状态
function lookLogistics() {
	if(client == "app") {
		document.location = "js://lookLogistics?params=jstojava";
		window.webkit.messageHandlers.lookLogistics.postMessage("123");
	}
}
//交互方法-查询物流状态
function paybackHome() {
	if(client == "app") {
		document.location = "js://paybackHome?params=jstojava";
		window.webkit.messageHandlers.paybackHome.postMessage("123");
	}
}
//交互方法-返回APP首页
function jumpMallIndex() {
	if(client == "app") {
		document.location = "js://jumpMallIndex?params=jstojava";
		window.webkit.messageHandlers.jumpMallIndex.postMessage("123");
	}
}

function getIosLocation() { //调用原生地区
	if(client == "app") {
		window.webkit.messageHandlers.getIosLocation.postMessage("getIosLocation");
	}
}

function getIosLocationData(region_id, region_name, region_name_full) { //接受原生地区数据
	if(client == "app") {
		if(!document.getElementById('showCityPickerP')) return false;
		if(!document.getElementById('region_id')) return false;
		if(!document.getElementById('region_name')) return false;
		document.getElementById('showCityPickerP').innerHTML = region_name_full;
		document.getElementById('showCityPickerP').value = region_name_full;
		document.getElementById('showCityPickerP').style.color = 'black';
		document.getElementById('region_id').value = region_id;
		document.getElementById('region_name').value = region_name;
		if(areaInfo) {
			var regionArray = region_name_full.split('/');
			areaInfo.province = regionArray[0];
			areaInfo.city = regionArray[1];
			areaInfo.area = regionArray[2];
		}
	}
}

function getIosHourMinute(type) { //调用原生时分数据
	if(client == "app") {
		window.webkit.messageHandlers.getIosHourMinute.postMessage(type);
	}
}

function getIosHourMinuteData(type, time) { //接受原生时分数据
	if(client == "app") {
		if(type) {
			if(type == "1") {
				if(!document.getElementById('business_sdate')) return false;
				document.getElementById('business_sdate').innerText = time;
				document.getElementById('business_sdate').value = time;
			} else if(type == "2") {
				if(!document.getElementById('business_edate')) return false;
				document.getElementById('business_edate').innerText = time;
				document.getElementById('business_edate').value = time;
			}
		}
	}
}

function getIosDate() { //调用原生日期
	if(client == "app") {
		//document.location="js://jumpMallIndex?params=jstojava";
		window.webkit.messageHandlers.getIosDate.postMessage("getIosDate");
	}
}

function getIosDateData(date) { //接受原生日期数据
	if(client == "app") {
		if(!document.getElementById('birthday')) return false;
		document.getElementById('birthday').innerText = date;
		document.getElementById('birthday').value = date;
	}
}

function pageShare() {

}
var client = getClient();
var clientType = getClientType();

function getClient() {
	/* APP内部头部增加yichun_ios，yichun_android关键字
	 * 
	 */
	var ua = window.navigator.userAgent.toLowerCase();
	if(ua.indexOf('yichun') > -1) {
		return "app";
	} else {
		if(ua.match(/MicroMessenger/i) == 'micromessenger') { //微信浏览器
			return 'weixin';
		} else { //其他时同微信
			return "H5";
		}
	}
}
if(client == 'weixin') { //微信端
	//非店员
	if(location.href.indexOf('wxLogin') > 0) {} else {
		if(localStorage.getItem('client_type')) { //店员
		} else {
			if(location.href.indexOf('list') == -1 &&
				location.href.indexOf('active') == -1 &&
				location.href.indexOf('cursor') == -1 &&
				location.href.indexOf('filter') == -1) {
				if(!localStorage.getItem('open_id')) {
					var code = GetRequest()['code'];
					if(!code) {
						if(localStorage.getItem('user_wxInfo')) {} else {
							localStorage.setItem('front_page', location.href); //微信认证后的跳转页面
							window.location.href = config.BASE_URL + "/wechat/oauth?state=app";
						}
					}
				} else if(!localStorage.getItem('userId') &&
					location.href.indexOf('phone') == -1 &&
					location.href.indexOf('list') == -1 &&
					location.href.indexOf('active') == -1 &&
					location.href.indexOf('cursor') == -1 &&
					location.href.indexOf('filter') == -1) {
					window.location.href = config.BASE_WECHAT + "/phone.html";
				}
			}
		}
	}
}

//客户端种类
function getClientType() {
	var ua = window.navigator.userAgent.toLowerCase();
	if(ua.indexOf('ios') > -1) {
		return 'ios';
	} else if(ua.indexOf('android') > -1) {
		return 'android';
	} else {
		return 'H5';
	}
}

function getparamHeader() {
	return {
		//客户端版本version，例：1.0.0
		version: '111', //false
		//zh_CN zh_CN
		locale: '', //false
		//手机系统版本（Build.VERSION.RELEAS）例：4.4，4.5
		os: '', //false
		//请求来源，例：android/ios/h5
		from: getClientType(), //true
		//手机尺寸，例：1080*1920
		screen: '', //false
		//机型信息（Build.MODEL），例：Redmi Note 3
		model: '', //false
		//渠道信息，例：com.wandoujia
		channel: '', //false
		//APP当前网络状态，例：wifi，mobile；部分接口可以根据用户当前的网络状态，下发不同数据策略，如：wifi则返回高清图，mobile情况则返回缩略图
		net: '', //false
		//APP唯一标识，有的公司一套server服务多款APP时，需要区分开每个APP来源
		appid: '', //false
		//SAAS平台，多商户 ID
		storeid: 'H5', //true
		//后台创建好之后直接写入数据库和客户端，不需要前端传参和后端参数返回
		//token : 'token'//true
		//sign:''//签名

	}
}

//object按Key排序
function paramSort(param) {
	var key = [];
	for(var k in param) {
		key.push(k);
	}
	key.sort();
	var temp = {};
	for(var i = 0; i < key.length; i++) {
		temp[key[i]] = param[key[i]];
	}
	return temp;
}

//ojbect转换成参数字符串（a=a&b=b....）
function paramToString(param) {
	var s = '';
	for(var k in param) {
		s += k + '=' + param[k] + "&";
	}
	//去除最后一个&
	s = s.substring(0, s.length - 1);
	s += '236TWX778T8MV90098F937GTQVKBDDFA'; //秘钥
	return s;
}

//合并对象
var extend = function(obj1, obj2) {
	var tempObj = new Object();
	for(var key in obj1) {
		tempObj[key] = obj1[key];
	}
	for(var key in obj2) {
		if(obj1.hasOwnProperty(key)) continue; //有相同的属性则略过
		tempObj[key] = obj2[key];
	}
	return tempObj;
}

function createApplyParam(applyParam) {
	// 处理对象(引用值) 受到影响的问题
	delete applyParam.header;
	var header = getparamHeader(); //获取共同参数头
	//var applyParam=getApplyParam({});//此次调用接口的参数,业务参数
	var allParam = $.extend({}, header, applyParam); //所有参数用于加密
	allParam = paramSort(allParam); //参数排序
	var allString = paramToString(allParam); //转换成加密字符串

	var sign = md5(allString); //加密
	header.sign = sign;
	applyParam.header = header;
	var p = JSON.stringify(applyParam);

	return p;
}


/**
 * 验证是否为手机号码（移动手机）
 *	=================================
 * @param {} source
 */
function fnIsMobilePhone(source) {
	var regex = /^1\d{10}$/;
    return regex.test(source);
}

/**
 * 验证是否为电子邮箱
 *	=================================
 * @param {}
 *            source
 */
function isEmail(source) {
    var regex = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
	if(source.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) != -1){
        return true;
    }else{
        return false;
    }
}


//获取地区列表
function getRegionList(callback) {
	cityPicker.setData(createCityData(sycCityData));
	if(!!callback) callback(sycCityData);

	/*
	var p=createApplyParam({});
	mui.ajax(serverAddress+'teamobi-api/api/region/getSubRegion',{
		data:{'json':p},
		dataType:'json',//服务器返回json格式数据
		type:'get',//HTTP请求类型
		timeout:10000,//超时时间设置为10秒；
		headers:{'Content-Type':'application/text'},	              
		success:function(data){
			cityPicker.setData(createCityData(data.data));
			if(!!callback)callback(data.data);
		},
		error:function(xhr,type,errorThrown){
			//异常处理；
			console.log(type);
		}
	});*/
}
//生成地区列表数据结构
function createCityData(data) {
	var cityData = [];
	for(var i = 0; i < data.length; i++) {
		var s = {
			value: data[i].code,
			text: data[i].name,
			children: []
		};
		for(var j = 0; j < data[i].data.length; j++) {
			var d = {
				value: data[i].data[j].code,
				text: data[i].data[j].name,
				children: []
			};
			for(var m = 0; m < data[i].data[j].data.length; m++) {
				var q = {
					text: data[i].data[j].data[m].name,
					value: data[i].data[j].data[m].code
				}
				d.children.push(q);
			}
			s.children.push(d);
		}
		cityData.push(s);
	}
	return cityData;
}

//图片上传start
//图片预览
function previewImage(file, img) {
	if(file.files.length == 0) return;
	showLoading();
	var tip = "请上传图片文件！"; // 设定提示信息 
	var prvbox = mui('img[forFile="' + img + '"]')[0];
	var f = file.files[0];
	if(window.FileReader) { // html5方案 
		//		var fr = new FileReader();
		//		fr.onload = function(e) {
		//			var src = e.target.result;
		//			console.log(src)
		//			if (!validateImg(src)) { 
		//				mui.alert(tip);
		//			} else { 
		//				showPrvImg(src,prvbox);
		//				uploadImg(img);
		//			}
		//		}
		//		fr.readAsDataURL(f);
		imgCompress(f, 500, function(base64) {
			showPrvImg(base64, prvbox);
			uploadImg(img, base64);
		})
	} else {
		//		if ( !/\.jpg$|\.png$|\.gif$/i.test(file.value) ) { 
		//			mui.alert(tip);
		//		} else { 
		//			uploadImg(img);
		//			showPrvImg(file.value,prvbox);
		//		}
		mui.toast('当前浏览器不能上传图片，谢谢~');
	}
}

function validateImg(data) {
	var filters = {
		"jpeg": "/9j/4",
		"gif": "R0lGOD",
		"png": "iVBORw"
	};
	var pos = data.indexOf(",") + 1;
	for(var e in filters) {
		if(data.indexOf(filters[e]) === pos) {
			return e;
		}
	}
	return null;
}

function showPrvImg(src, prvbox) {
	prvbox.src = src;
}

function imgCompress(file, maxLen, callBack) {
	var img = new Image();
	var imgType;
	var reader = new FileReader(); //读取客户端上的文件
	reader.readAsDataURL(file);
	reader.onload = function(e) {
		var url = e.target.result; //读取到的文件内容.这个属性只在读取操作完成之后才有效,并且数据的格式取决于读取操作是由哪个方法发起的.所以必须使用reader.onload，
		imgType = validateImg(url);
		if(!validateImg(url)) {
			mui.alert('请上传图片文件！');
			return false;
		} else {
			img.src = url; //reader读取的文件内容是base64,利用这个url就能实现上传前预览图片
		}
	};
	img.onload = function() {
		//生成比例
		var width = img.width,
			height = img.height;
		//计算缩放比例
		var rate = 1;
		if(width >= height) {
			if(width > maxLen) {
				rate = maxLen / width;
			}
		} else {
			if(height > maxLen) {
				rate = maxLen / height;
			}
		};
		img.width = width * rate;
		img.height = height * rate;
		//生成canvas
		var canvas = document.createElement("canvas");
		canvas.width = img.width;
		canvas.height = img.height;
		var ctx = canvas.getContext("2d");
		ctx.drawImage(img, 0, 0, img.width, img.height);
		if(imgType == 'png') { //png图片生成png
			var base64 = canvas.toDataURL('image/png', 0.9);
		} else {
			var base64 = canvas.toDataURL('image/jpeg', 0.9);
		}

		callBack(base64);
	};
}

function uploadImg(img, base64Codes) {
	//图片上传
	var formData = new FormData();
	formData.append("file", convertBase64UrlToBlob(base64Codes));
	formData.append("type", '1');

	jQuery.ajax({
		url: serverAddress + 'teamobi-api/api/common/uploadImage',
		type: "POST",
		data: formData,
		dataType: "text",
		processData: false, // 告诉jQuery不要去处理发送的数据  
		contentType: false, // 告诉jQuery不要去设置Content-Type请求头
		success: function(e) {
			var info = JSON.parse(e);
			closeLoading();
			if(info.header.returnCode == 1) {
				mui.toast('上传成功');
				mui('img[forFile="' + img + '"]')[0].setAttribute('uploadSrc', info.data.url);
			} else {
				mui.toast('上传失败');
			}
		},
		xhr: function() { //在jquery函数中直接使用ajax的XMLHttpRequest对象  
			var xhr = new XMLHttpRequest();

			xhr.upload.addEventListener("progress", function(evt) {
				if(evt.lengthComputable) {
					var percentComplete = Math.round(evt.loaded * 100 / evt.total);
					console.log("正在提交." + percentComplete.toString() + '%'); //在控制台打印上传进度  
				}
			}, false);

			return xhr;
		}
	});

	//	jQuery("#uploadForm_"+img).ajaxSubmit({
	//		type: 'post',//提交方式  
	//		timeout:100000,
	//		dataType : 'json',
	//  	url:  serverAddress+'teamobi-api/api/common/uploadImage',
	//  	success: function(e) {
	//  		closeLoading();
	//  		if(e.header.returnCode==1){
	//  			mui.toast('上传成功');
	//  			mui('img[forFile="'+img+'"]')[0].setAttribute('uploadSrc',e.data.url);
	//  		}else{
	//  			mui.toast('上传失败');
	//  		}
	//  	},
	//		error:function(e){
	//			console.log(e);
	//			mui.toast('上传失败');
	//			closeLoading();
	//		}
	//	});
}

function convertBase64UrlToBlob(urlData) { //base64转blob对象

	var bytes = window.atob(urlData.split(',')[1]); //去掉url的头，并转换为byte  

	//处理异常,将ascii码小于0的转换为大于0  
	var ab = new ArrayBuffer(bytes.length);
	var ia = new Uint8Array(ab);
	for(var i = 0; i < bytes.length; i++) {
		ia[i] = bytes.charCodeAt(i);
	}

	return new Blob([ab], {
		type: 'image/png'
	});
}

//图片上传end


/*
 *支付方式
 *1：现金支付 2、支付宝支付 3、微信支付 4、pos刷卡 5、易币 6、支付宝+eb 7、微信+eb
 */
function getPayTypeString(id) {
	var s = '';
	switch(id) {
		case '1':
			s = '现金支付';
			break;
		case '2':
			s = '支付宝支付';
			break;
		case '3':
			s = '微信支付';
			break;
		case '4':
			s = 'pos刷卡';
			break;
		case '5':
			s = '易币';
			break;
		case '6':
			s = '支付宝+易币';
			break;
		case '7':
			s = '微信+易币';
			break;
		default:
			break;
	}
	return s;
}

var maskFlg = false;
var mask;
//显示loading
function showLoading() {
	if(mui('.loadEffect').length == 0) {
		mui("body")[0].appendChild(createLoading());
	} else {
		mui(".loadEffect")[0].style.display = "block";
	}
	//遮罩
	mask = mui.createMask(function() {
		return maskFlg;
	});
	mask.show();
}
//生成loading
function createLoading() {
	var loading = document.createElement('div');
	loading.className = 'loadEffect';
	//loading.innerHTML='<span></span> <span></span> <span></span> <span></span> <span></span> <span></span> <span></span> <span></span>';
	//<div class="loadEffect"> <span></span> <span></span> <span></span> <span></span> <span></span> <span></span> <span></span> <span></span> </div>
	return loading;
}
//关闭loading
function closeLoading() {
	//加载完成隐藏遮罩
	if(mui(".loadEffect").length > 0) {
		mui(".loadEffect")[0].style.display = "none";
		maskFlg = true;
		mask.close();
	}
}

function showDiyMask() {
	//遮罩
	mask = mui.createMask(function() {
		return maskFlg;
	});
	mask.show();
}

function setImgWidth(id) {
	mui('#' + id + ' img').each(function() {
		this.setAttribute('width', '100%');
	})
}

//弹出透明遮罩，防止连续多次点击
function showDrop() {
	if(mui('.syc-backdrop').length == 0) {
		var drop = document.createElement('div');
		drop.className = 'syc-backdrop';
		mui("body")[0].appendChild(drop);
		setTimeout(function() {
			drop.remove();
		}, 500);
	}
}

/**
 * 清除字符串换行与空格
 * @param {Object} str
 */
function replaceHtml(str) {
	str = str.replace(/\r/g, "");
	str = str.replace(/\n/g, "");

	return str;
}

/**
* 验证纯中文
*/
function isChinaName(name) {
	var pattern = /^[\u4E00-\u9FA5]$/;
	return pattern.test(name);
}

/**
* 验证纯数字
*/ 
function isArabicNumerals(_number) {
	var pattern = /^[0-9]+$/;
	return pattern.test(_number);
}


/**
* 转换时间戳为   年/月/日
*/
function timeFormat(nS) { 	
	return new Date(parseInt(("/Date("+nS+")/").substr(6, 13))).toLocaleDateString(); 
};

/**
 * 时间戳 转化为: "1970-01-17" 或者 "yyyy-MM-dd hh:mm:ss"  格式 | 日期
 * @param {Object} theDate	时间, new data
 * @param {Object} _format	格式, 可能的值为month; 如果为 month, 则为 年月日, 否则扩展到 时分秒
* ======================================
* 调用方法:
* fnFormat(new Date(1403149534) [,_format] )
*/
function fnFormat(theDate, _format){
	var format = 
		_format === "month" ? "yyyy-MM-dd" : "yyyy-MM-dd hh:mm:ss";
	var theDate = new Date(+theDate);
    var o = {
        "M+" : theDate.getMonth()+1, //month
        "d+" : theDate.getDate(),    //day
        "h+" : theDate.getHours(),   //hour
        "m+" : theDate.getMinutes(), //minute
        "s+" : theDate.getSeconds(), //second
        "q+" : Math.floor((theDate.getMonth()+3)/3),  //quarter
        "S" : theDate.getMilliseconds() //millisecond
    };

    if(/(y+)/.test(format)) format=format.replace(RegExp.$1,
(theDate.getFullYear()+"").substr(4 - RegExp.$1.length));
    for(var k in o){
        if(new RegExp("("+ k +")").test(format))
            format = format.replace(RegExp.$1,RegExp.$1.length==1 ? o[k] :("00"+ o[k]).substr((""+ o[k]).length));
    }
    return format;
}

// ===========================================================================
// ===========================================================================
// ===========================================================================


window.COMMON = new Object(); 

/**
 * 根据数据(对象) 返回一个 json=* ,包含 header(已加密的) 的字符串
 * ===================================================
 * @param {*Object} options	需要加密的字符串
 * @param {Object} param	一些不需要加密的字符串
 */
COMMON.fnReturnAjaxData = function(options){
	var _options = $.extend(true, {}, options);
	var md5word = createApplyParam(_options)

	_options = $.extend(true, options, JSON.parse(md5word) )
	_options.header.accessToken = (options && options.header && options.header.accessToken) || sessionStorage.getItem("accessToken");
	return 'json='+ JSON.stringify(_options) ;
}



/**
 * 分页数据整合求得数据
 * =====================================================
 * @param {*JqueryDom} $dom		jquery对象, 分页插件的 dom盒子
 * @param {*Object} dataBox		数据列表对象
 * 		page					当前页
 * 		count					总数据条数
 * 		pageSize				每页多少条数据
 * @param {Function} callback	回调函数, 内部参数为分页插件点击的当前页
 */
COMMON.fnSetPageList = function($dom, dataBox, callback){
	$dom.paging({
		pageNo:	dataBox.page,		
		totalPage: Math.ceil(dataBox.count / dataBox.pageSize),	
		totalSize: dataBox.count , 
		callback: function(num) {
			
			console.warn("*分页数据: " ,num) // TODO : 上线时删除
			
			if(typeof callback === "function"){
				callback(num)
			}
		}
	})
	return true;
}

/**
 * 设置弹出模态框的 文本内容
 * =====================================================
 * @param {Object} options
 *     @param {String} id
 *     @param {String} title
 *     @param {String} innerhtml
 * 
 * =====================================================
 * <div class="modal fade bs-example-modal-sm" id="example" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel"></div>
 * 
 * =====================================================
 * 说明:
 * 	如果没有知道取消的函数, 则: 取消按钮不会显示
 */
COMMON.fnSetModal = function(options){
	var theDomData = $.extend(true, {
		id : parseInt(Math.random()*(1-10000)+10000),
		title	: "提示",
		innerhtml :  "" 
	}, options);
	
	var domHtml = 
	'<div id="'+ theDomData.id +'" class="modal fade bs-example-modal-sm" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel">'+
	'	<div class="modal-dialog modal-sm" role="document" style="margin:240px auto;">'+
	'        <div class="modal-content" style="width:300px;border-radius:4px;">'+
	'            <div class="modal-header" style="background:rgb(58, 211, 232);padding:0 0 0 16px;;border-bottom:none;height:40px;border-top-left-radius:4px;border-top-right-radius:4px;">'+
	// '                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true" style="color:#fff;">&times;</span></button>'+
	'                <div class="modal-title" id="exampleModalLabel" style="font-size:14px;color:#fff;line-height:40px;"> '+ theDomData.title +'</div>'+
	'            </div>'+
	'            <div class="modal-body" style="padding:0px;">'+
	'                <form>'+
	'                    <div class="form-group" style="margin-bottom:10px;">'+
	'                        <!-- <label for="recipient-name" class="control-label">textarea</label> -->'+
	'                        <!--<button type="text" class="qing-date-input input-sm input-l datetimepicker-input form-control" id="" name=""  value="" placeholder="请选择到访时间" readonly>请选择到访时间</button>-->'+
	'                        <h3 style="text-align:center;font-size:14px;color:rgb(58, 211, 232);margin:0;line-height:60px;"> '+ theDomData.innerhtml +' </h3>'+
	'                    </div>'+
	'                </form>'+
	'            </div>'+
	'            <div class="modal-footer" style="border-top:none;text-align:center;padding:0 15px 10px;">'+
	'				 <button id="cancel-'+ theDomData.id +'" type="button" class="btn d-n" data-dismiss="modal" aria-label="Close" style="background-color:#3ad3e8;color:#fff;">取消</button>'+
	'                <button id="ensure-'+ theDomData.id +'" type="button" class="btn" data-dismiss="modal" style="margin-left:0;background:rgb(58, 211, 232);width:56px;height:25px;font-size:12px;color:#fff;padding:0;" >确定</button>'+
	'            </div>'+
	'        </div>'+
	'    </div>'+
	'</div>';

	var $dom = $(domHtml);
	$dom.theDomData = theDomData;
	$dom.fnSetInit = function(){
		$(this).find(".modal-header h4").html(theDomData.title)
		$(this).find(".modal-body h3").html(theDomData.innerhtml)
		return $dom;
	}
	$dom.fnSetTitle = function(str){
		$(this).find(".modal-header h4").html(str)
		return $dom;
	}
	$dom.fnSetInnerHtml = function(str){
		$(this).find(".modal-body h3").html(str)
		return $dom;
	}
	$dom.fnSetCancel = function(calllback){
		$(this).find('#cancel-'+ theDomData.id).show().click(calllback)
		return $dom;
	}
	$dom.fnSetEnsure = function(calllback){
		$(this).find('#ensure-'+ theDomData.id).click(calllback)
		return $dom;
	}

	$dom.appendTo($("body"))
	return $dom;
}



/**
 * 为页面绑定 回车事件
 * @param {Object} callback
 */
COMMON.fnEventEnter = function(callback){
	$(document).on("keydown",function(event){
		if(event.keyCode === 13){
			callback();
			event.stopPropagation();
			event.preventDefault();
			return true;
		}
	})
}



/**
 * 为页面绑定 esc 事件
 * @param {Object} callback
 */
COMMON.fnEventEsc = function(callback){
	$(document).on("keydown",function(event){
		if(event.keyCode === 27){
			callback();
			event.stopPropagation();
			event.preventDefault();
			return true;
		}
	})
}


/**
 * 获取地址栏指定参数 | 地址栏参数 | url参数
 * =====================================================
 * 地址栏参数例: customer_orderInfo_edit.html?type=compile&id=e9f874cb59534df5ba398056c93bf8a3&v=1
 */
function GetQueryString(name){
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if(r!=null){
        return  unescape(r[2]); 
    }else{
        return null;
    }
}

/*
 * 获取url参数
 */
// function GetRequest() {
// 	var url = location.search; //获取url中"?"符后的字串 
// 	var theRequest = new Object();
// 	if(url.indexOf("?") != -1) {
// 		var str = url.substr(1);
// 		strs = str.split("&");
// 		for(var i = 0; i < strs.length; i++) {
// 			theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
// 		}
// 	}
// 	return theRequest;
// }

/**
 * 小于10自动补零, 小于十
 * =====================================================
 * 如: 数字"1" 转为字符串 "01"
 */
function addZero(s) {
	var _s = Number(s);
    return _s < 10 ? '0' + _s : _s;
}

/**
 * 获取当前时间
 * =====================================================
 * 格式: "2017-11-27 18:20:03"
 */
function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
	var seperator2 = ":";
	var month = date.getMonth() + 1;
	var strDate = date.getDate();
	// if (month >= 1 && month <= 9) {
	//     month = "0" + month;
	// }
	// if (strDate >= 0 && strDate <= 9) {
	//     strDate = "0" + strDate;
	// }
	var currentdate = date.getFullYear() + seperator1 + addZero(month) + seperator1 + addZero(strDate)
        + " " + addZero(date.getHours()) + seperator2 + addZero(date.getMinutes())
            + seperator2 + addZero(date.getSeconds());
    return currentdate;
}

/**
 * 获取当前日期(年-月-日)
 * =====================================================
 * 格式: "2017-11-27"
 */
function getNowDate() {
    var date = new Date();
    var seperator1 = "-";
	var month = date.getMonth() + 1;
	var strDate = date.getDate();
	var currentdate = date.getFullYear() + seperator1 + addZero(month) + seperator1 + addZero(strDate);
    return currentdate;
}


/**
 * 判断数据是否存在
 * =================================
 * @param {string} param
 * @param {string} paramDesc
 * =================================
 * 说明:
 * 	2个参数都存在, 第一个参数为 判断依据, 一般是字段, 如果成立, 则使用参数2
 *  2个参数只存在一个参数, 则判断此参数是否成立, 如果成立则返回此字段
 */
COMMON.fnTypeCompareData = function (param, paramDesc){
	var _paramDesc = !!paramDesc ? paramDesc : param;
	
	return (CRM.fnTypeCompare(param) ? _paramDesc : "暂无");
}


/**
 * 分配人为空显示空字符串
 * @param {*} param 
 * @param {*} paramDesc 
 */
COMMON.fnTypeCompareAssignor = function (param, paramDesc){
	var _paramDesc = !!paramDesc ? paramDesc : param;
	
	return (CRM.fnTypeCompare(param) ? _paramDesc : "");
}




/**
* 函数说明：给数字加千分位显示
* 参数说明：num   需要加千分位的数字
* ============================================
* @param{*Object}
* ============================================
* @return
*/
COMMON.fnnumToThousandsSeparator = function (num) {
	//如果传进来的值不是数字，则原值返回
	if (!Number(num) || num < 1000) {
		return num;
	}
	num = num + "";
	var re = /(-?\d+)(\d{3})/;
	//正则判断
	while (re.test(num)) {
		//符合条件则进行替换
		num = num.replace(re, "$1,$2");
	}
	return num;
}



/**
* 针对 Object 进行 fliter 操作
* ============================================
* @param{*Object}
* ============================================
* @return  Object -> 经过过滤操作的 Obj 对象
*/
COMMON.fnfilterObj = function(obj, func) {
	let ret = {};
	for(let key in obj) {
	  if(obj.hasOwnProperty(key) && func(obj[key], key)) {
		ret[key] = func(obj[key], key) || obj[key];
	  }
	}
	return ret;
}


/**
* 根据 图片路径 获得BASE64编码
* ============================================
* @param {*String}
* ============================================
* @return  Object -> 经过操作返回的 base 字符串
*/
COMMON.fnImageToBase64 = function(imgSrc) {
    var img = new Image();   
		img.src = imgSrc;
	var canvas = document.createElement("canvas");
	var context = canvas.getContext("2d");
		// 绘制图片到canvas上   
		canvas.width = img.width;   
		canvas.height = img.height;   

		// 在canvas绘制前填充白色背景   
		context.fillStyle = "#fff";   
		context.fillRect(0, 0, canvas.width, canvas.height);   
		context.drawImage(img, 0, 0);
	return canvas.toDataURL();
}




/**
* 获得 并设置 员工列表select选择
* ============================================
* @param{*Object} options 相关参数
* ============================================
* @return
*/
COMMON.fnGetEmployeeList = function(options) {
	var pushData = Object.assign({
		"orgId": YiMengYun.ORGID
		, "shopId": YiMengYun.SHOPID
		, "userId": YiMengYun.USERID
		, "departmentId": options.departmentId
		, pageIndex: '1'
		, pageSize: '1000'
	}, options)
	pushData = fnClearEmptyInObj(pushData);
	return new Promise((resolve, reject) => {
		YiMengYun.fnDataClient(
			{
				Route: "/api/staff/staffList"
				, type: 'post'
				, data: pushData
			}
			, function (resp) {
				resolve(resp)
			}
			, function (resp) {
				reject(resp)
			}
		)
	});
}



/**
* 待使用 | 待使用
* ============================================
* @param{*Object} options 相关参数
* ============================================
* @return
*/
COMMON.fnGetReportQuery = function(options) {
	var pushData = Object.assign({
		"orgId": YiMengYun.ORGID
		, "shopId": YiMengYun.SHOPID
		, "userId": YiMengYun.USERID
		, type : ''
	}, options)
	pushData = fnClearEmptyInObj(pushData);
	return new Promise((resolve, reject) => {
		YiMengYun.fnDataClient(
			{
				Route: "/api/report/reportQuery"
				, type: 'post'
				, cache : false
				, data: pushData
			}
			, function (resp) {
				resolve(resp)
			}
			, function (resp) {
				reject(resp)
			}
		)
	});
}


/**
* 把 小数 number转化成百分比且百分比之后只保留2位小数
* ============================================
* @param{*Number} num 数值
* ============================================
* @return String||Boolean  (百分比字符串 || false)
*/
function fnNumberToPercent(num){
	if(typeof num === 'number'){
		return (Math.round(num * 10000)/100).toFixed(2) + '%';
	}
	else{
		return false
	}
}


/**
 * 相等比较
 * @param {Object} value 
 * @retruns [Boolean]
 */
function fnTypeCompare(value) {
	try {
		switch(value) {
			case "false":
			case false:
			case undefined:
			case "undefined":
			case null:
			case "null":
			case 0:
			case "0":
			case "":
			case "{}":
			case "[]":
				return false;
				break;
			default:
				return true;
				break;
		}
	} catch(err) {
		console.error(err)
	}
}

/**
 * 判断字符串是否为空
 * @param {Object} value 
 * @retruns [Boolean]
 */
function fnEmptyCompare(value) {
	try {
		switch(value) {
			case "false":
			case false:
			case undefined:
			case "undefined":
			case null:
			case "null":
			//case 0:
			//case "0":
			case "":
			case "{}":
			case "[]":
				return false;
				break;
			default:
				return true;
				break;
		}
	} catch(err) {
		console.error(err)
	}
}

/**
 * console.log 
 * =====================================
 * @param {Object} obj	
 */
function fnLog() {
	console.log("😀::---");
	for (var index = 0; index < arguments.length; index++) {
		var element = arguments[index];
		console.log(element.toString(), ": \n\n " ,element,  "| typeof 此值的类型 为 " + typeof element);
	}
	return arguments;
}



/**
* 将对象中的空数据 delete
* ============================================
* @param{*Object} 需要清理的数据
* ============================================
* @return  Object
*/
function fnClearEmptyInObj(obj){
	var obj = Object.assign({}, obj)
	for (var key in obj) {
		if (obj.hasOwnProperty(key)) {
			var element = obj[key];
			if(!fnEmptyCompare(element) || !element){
			 	delete obj[key];
			}
		}
	}
	return obj;
}


/**
* 加载 内部样式, 注入style标签在 head 后
* ============================================
* @param{*Object} 需要清理的数据
* ============================================
* @return  Object
*/
function fnLoadStyleCode(code){
    var style = document.createElement("style");
    style.type = "text/css";
    try{
        // Firefox Opera Safari
        style.appendChild(document.createTextNode(code));
    }catch(er){
        // IE
        style.stylesheet.cssText = code;
	}
	style.id = new Date().getTime();
    document.head.appendChild(style)
    return style;
}



/**
 * 用于 日期插件的 中文显示
 */
;(function($){
	// $.fn.datetimepicker.dates['zh-CN'] = {
	// 		days: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"],
	// 		daysShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六", "周日"],
	// 		daysMin:  ["日", "一", "二", "三", "四", "五", "六", "日"],
	// 		months: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
	// 		monthsShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
	// 		today: "今日",
	// 		suffix: [],
	// 		meridiem: ["上午", "下午"],
	// 		autoclose:true
	// };
}(jQuery));