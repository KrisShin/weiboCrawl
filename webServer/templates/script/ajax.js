

/**
* 登录
* ============================================
* @param{*Object} options 相关参数
* ============================================
* @return
*/
function fnLogin(options) {
	var pushData = Object.assign({}, options)
	pushData = fnClearEmptyInObj(pushData);
	return new Promise((resolve, reject) => {
        $.ajax({
            type: "POST",
            url: "",
            data: "",
            success (response) {
                
            },
            error (response){

            }
        });
	});
}