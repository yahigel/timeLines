$(function()
{
	//バリデーション
	$('#id_項目数').on('blur',function()
	{
		let error;
		let value = $(this).val();
		if($.isNumeric(value) != true)
		{
			error = true;
		}
		if(value > 500)
		{
			error = true;
		}
		if(error)
		{
			//エラー時の処理s
				$('#createButton').prop("disabled", true);
		}else{
				$('#createButton').prop("disabled", false);
		}
	});

	$(window).scroll(function (){
		$(".dekigoto").each(function(){
			var imgPos = $(this).offset().top;
			var scroll = $(window).scrollTop();
			var windowHeight = $(window).height();
			if (scroll > imgPos - windowHeight + windowHeight/5){
				$(this).addClass("fade_on");
			} else {
				$(this).removeClass("fade_on");
			}
		});
	});

	var showFlag = false;
	var topBtn = $('#page-top');
	topBtn.css('bottom', '-100px');
	var showFlag = false;
	//スクロールが100に達したらボタン表示
	$(window).scroll(function () {
			if ($(this).scrollTop() > 100) {
					if (showFlag == false) {
							showFlag = true;
							topBtn.stop().animate({'bottom' : '20px'}, 200); 
					}
			} else {
					if (showFlag) {
							showFlag = false;
							topBtn.stop().animate({'bottom' : '-100px'}, 200); 
					}
			}
	});
	//スクロールしてトップ
	topBtn.click(function () {
			$('body,html').animate({
					scrollTop: 0
			}, 500);
			return false;
	});
});
