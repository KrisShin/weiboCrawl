/*  header-comment
/*  file   : /Users/abbyispeng/Desktop/Dinstall/outsource/+Java仿新浪首页/high_imitation_sina/script/build
/*  author : QingGuiPeng
/*  date   : 2018-3-28 15:40:11
/*  last   : 2018-4-5 22:7:53
*/

// Qing
$(document).ready(function () {
    // 点击 `账号登录` 或  `账号注册` 又或 '我的信息'
    $(document).on('click', '.loginAndReg-box a[data-prop="login_and_reg"]', function () {
        $(this).addClass('cur W_fb').siblings().removeClass('cur W_fb');
        var _text = $(this).text();
        console.log(
            _text
        );
        // 显示 登陆注册的dom
        $('#loging-reg-infoBox').show();
        $('#my_info_box').hide();
        switch (_text) {
            case '账号登录':
                $('#LoginRegistrationField').text('登录');
                break;
            case '账号注册':
                $('#LoginRegistrationField').text('注册');
                break;
            case '我的信息':
                // 显示 我的信息 的dom
                $('#loging-reg-infoBox').hide();
                $('#my_info_box').show();
                break;
            default:
                break;
        }
        event.preventDefault();
        event.stopPropagation();
    });

    // 点击登录 或 注册
    $(document).on('click', '#LoginRegistrationField', function () {
        // $('#loginname').val(''); // 账号
        // $('#password').val('');  // 密码

        switch ($(this).text()) {
            case '登录':
                alert('登录成功!')
                break;
            case '注册':
                alert('注册成功!')
                break;
            default:
                break;
        }

        // 显示 我的信息 的dom
        $('#loginname').val('');
        $('#password').val('');
        $('#loging-reg-infoBox').hide();
        $('#my_info_box').show();
        event.preventDefault();
        event.stopPropagation();
    });

    // 点击注销
    $(document).on('click', '#my_DropOut', function () {
        $('#loging-reg-infoBox').show();
        $('#my_info_box').hide();
        event.preventDefault();
        event.stopPropagation();
    });

    // 点击 action-type="close" 则
    // 设置父级含有 action-type 属性的元素为 display为none
    $(document).on('click', '*[action-type="close"]', function () {
        $(this).parents('*[action-type]').hide();

        event.preventDefault();
        event.stopPropagation();
    });

    // 发帖子 点击 `发表`
    $(document).on('click', '#fabiao', function () {
        let sFabiaoTitle = $('#fabiaoTitle').val();;
        let  sFabiaoContent =$('#fabiaoContent').val();;


        alert(
            '帖子表头: ' + sFabiaoTitle
        )
        alert(
            '帖子内容: ' + sFabiaoContent
        )
        location.reload();
        event.preventDefault();
        event.stopPropagation();
    });

    // 更新文档
    $(document).on('click', '#updatePage', function () {
        alert('更新了文档');
        event.preventDefault();
        event.stopPropagation();
        $('#updatePage').hide();
    });

    // 点击刷新那个按钮
    $(document).on('click', '#base_reload', function () {
        location.reload();
        event.preventDefault();
        event.stopPropagation();
    });

    // 点赞
    $(document).on('click', '.subinfo_dianzan', function () {
        let nCount = +($(this).find('em').eq(1).text());
        $(this).css({
            'color': '#eb7350'
        })
        $(this).find('em').eq(0).css({
            'color': '#eb7350'
        })
        alert('点赞加一')
        nCount++;
        $(this).find('em').eq(1).text(nCount);
        $(this).removeClass('subinfo_dianzan');

        event.preventDefault();
        event.stopPropagation();
    });

    // 发表评论
    $(document).on('click', '#fabiaoPlun-btn', function () {
        let sFabiaoPlunContent = $('#fabiaoPlun-content').val();
        $('#fabiaoPlun-content').val('');
        alert(
            '评论内容' + sFabiaoPlunContent
        )
        event.preventDefault();
        event.stopPropagation();
    });

    // 点击搜索按钮
    $(document).on('click', '#search-btn', function () {
        alert('搜索内容: ' + sSearchText)
        let sSearchText = $('#search-ipt').val();
        event.preventDefault();
        event.stopPropagation();
    });

    // 点击购买会员
    $(document).on('click', '#purchaseMember', function () {
        
        alert('购买会员成功!')
        event.preventDefault();
        event.stopPropagation();
    });
    
});
