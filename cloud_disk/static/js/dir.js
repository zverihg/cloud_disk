String.prototype.format = function ( arguments ) {
	var this_string = '';
	for ( var char_pos = 0; char_pos < this.length; char_pos++ ) {
		this_string = this_string + this[char_pos];
	};
	for ( var key in arguments ) {
		var string_key = '{'+key+'}';
		this_string = this_string.replace( new RegExp( string_key, 'g' ), arguments[key] );
	};
	return this_string;
};

function unbin( a ) {
	return a
	.split(' ')
	.map( bin => String.fromCharCode(parseInt(bin, 2)) )
	.join('');
};

function onbin(a) {
    return a
    .split('')
    .map( cha => cha.charCodeAt(0).toString(2) )
    .join(' ');
};

function redraw_form_body_scrollbar() {

	$( '.scr_bar' ).mCustomScrollbar({
		scrollButtons		: { enable: true, scrollType: 'stepped' },
		scrollInertia		: 0,
		keyboard			: { scrollType : 'stepped' },
		mouseWheel			: { scrollAmount : 50 },
		theme				: 'dark-thin',
		autoExpandScrollbar	: false,
		autoHideScrollbar	: false,
		alwaysShowScrollbar	: 1,
	});

};

$(document).ready(function() {

	del_tme = 100

	ovr_blk_shw(); 

	setTimeout( ctl_exe___xls_upl, del_tme );


	$('.cnx_mne'		).css( 'display', 'none');

	window.addEventListener("orientationchange", function() { adj_hgh() }, false);

	// $(document).click(function() {$('.cnx_mne').hide()})
	
	$('.lst_dir').on('click', '.dir_itm_nme',	function(){	get_dir($(this));		});
	$('.lst_dir').on('click', '.dir_itm_ext',	function(){	get_dir($(this));		});
	$('.lst_dir').on('click', '.del_fil',		function(){	del_fil($(this));		});
	$('.dir_hdr').on('click', '.hom_dir',		function(){	get_dfl_dir();			});
	$('.dir_hdr').on('click', '.bck_dir',		function(){	get_bck_dir();			});
	$('.dir_hdr').on('click', '.ind_sta',		function(){	chk_con();				});
	$('.rnm_cnt').on('click', '.btn_sbm',		function(){	rnm_sbm();				});
	$('.rnm_cnt').on('click', '.btn_cnc',		function(){	$('.rnm_cnt').hide()	});

	redraw_form_body_scrollbar();

	var input_foverwork = document.getElementById( 'foverwork' );
	var infoArea_foverwork = document.getElementById( 'foverwork-filename' );
	input_foverwork.addEventListener( 'change', function(event) {ovr_blk_shw(); setTimeout( showFileName_foverwork, del_tme, event, ); ovr_blk_hde();} );
	function showFileName_foverwork( event ) {

		var input = event.srcElement;
		var fileName = input.files[0].name;
		infoArea_foverwork.textContent = '' + fileName;

		var formData = new FormData();
		formData.append('fil_pth', $(".now_dir").text());
		formData.append('file', $("#foverwork")[0].files[0]);

		$.ajax({
			type: "POST", 
			url: "/dir/snt_fil",
			cache: false,
			contentType: false,
			processData: false,
			data: formData,
			success: function(data){res_dta = data;},
			error: function(data){alert( 'boi oh boi, nth happen!' );},
			dataType: 'json',
			async: false,
			timeout: 600000,
		});

		rld_dir();


	}

	adj_hgh();

});


$(document).ready(function() {

	$(function(){
		$('.lst_dir').contextMenu({
			selector: '.dir_itm_cnt',
			callback: function(key, options) {

				if (key == 'del'){ 
					del_fil($(this))
				}				
		
				if (key == 'dwn'){ 

					dir_cnt = $(this).closest('.dir_itm_cnt')

					var res;
					dir_nme = $(dir_cnt).find('.nme').text()
					dir_ext = $(dir_cnt).find('.dir_itm_ext').text()


					var res;
					now_dir = $('.now_dir').text();
					dta = {"now_dir": now_dir, "dir_nme": dir_nme, 'ext': dir_ext}

					$.ajax({
						  type: "POST", 
						  url: "/dir/dwn_fil",
						  data: dta,
						  success: function(data){	res = data;  },
						  // dataType: 'json',
						  async: false,
						  timeout: 600000,
						});

						var x=window.open();
						doc_lnk =  JSON.parse(res).dta;
						x.document.location.replace(doc_lnk)

				}

				if (key == 'rnm'){
					
					$('.rnm_cnt').show();
					$('.rnm_cnt').addClass('usr_sel')


					dir_cnt = $(this).closest('.dir_itm_cnt')

					var res;
					dir_nme = $(dir_cnt).find('.nme').text()
					dir_ext = $(dir_cnt).find('.dir_itm_ext').text()
					
					fil_nme = $('.now_dir').text() + dir_nme
					$('.rnm_nme_inp')[0].value = dir_nme

					$('.met_rnm').text(dir_nme)

				}


			},
			items: {
				"rnm": {name: "Переименовать", icon: "edit"},
				"del": {name: "Удалить", icon: "edit"},
				"dwn": {name: "Скачать", icon: "edit"},

				"sep1": "---------",
				"quit": {name: "Закрыть", icon: function($element, key, item){ return 'context-menu-icon context-menu-icon-quit'; }}
			}
		});
	});
});

$(document).keyup(function(e) {
	if (!$('.rnm_cnt').hasClass("usr_sel"))
	{
		
		if (e.key == "Backspace"	|| e.keyCode === 8	){get_bck_dir();}
		if (e.key == "Home"			|| e.keyCode === 36	){get_dfl_dir();}
		if (e.key == "ArrowDown"	|| e.keyCode === 40	){
			
			itm = $('.lst_dir').find('.usr_sel');
			if(itm.length == 0){
				foc = $('.lst_dir').children(":first")
				foc.css('background-color', '#00f7ff26')
				foc.addClass('usr_sel')
			}else{
				if(itm.next().length > 0){
					itm.css('background-color', '#5f9ea026')
					itm.removeClass('usr_sel')
					itm.next().addClass('usr_sel')
					itm.next().css('background-color', '#00f7ff26')
				}
			}
		}
		if (e.key == "ArrowUp"		|| e.keyCode === 38	){
			
			itm = $('.lst_dir').find('.usr_sel');
			if(itm.length == 0){
				foc = $('.lst_dir').children(":first")
				foc.css('background-color', '#00f7ff26')
				foc.addClass('usr_sel')
			}else{
				if(itm.prev().length > 0){
					itm.css('background-color', '#5f9ea026')
					itm.removeClass('usr_sel')
					itm.prev().addClass('usr_sel')
					itm.prev().css('background-color', '#00f7ff26')
				}
			}

		}

		if (e.key == "Enter"		|| e.keyCode === 13	){
			itm = $('.lst_dir').find('.usr_sel');
			if(itm.length > 0){get_dir(itm)}
			foc = $('.lst_dir').children(":first")
			foc.css('background-color', '#00f7ff26')
			foc.addClass('usr_sel')
			
		}
	}

});

function snt_fil_cnt(event, infoArea_foverwork){

	var input = event.srcElement;
	var fileName = input.files[0].name;
	infoArea_foverwork.textContent = '' + fileName;

	var formData = new FormData();
	formData.append('fil_pth', $(".now_dir").text());
	formData.append('file', $("#foverwork")[0].files[0]);

	$.ajax({
		type: "POST", 
		url: "/dir/snt_fil",
		cache: false,
		contentType: false,
		processData: false,
		data: formData,
		success: function(data){res_dta = data;},
		error: function(data){alert( 'boi oh boi, nth happen!' );},
		dataType: 'json',
		async: false,
		timeout: 600000,
	});

	rld_dir();
}

function adj_hgh(){
	wdh		= window.screen.width;
	hgh		= window.screen.height;
	phn_ori	= window.orientation;

	// console.log(phn_ori)

	if ( wdh <=  500){
		$('.tbl_bdy'		).css( 'top',		'13em'	);
		$('.scr_bar'		).css( 'top',		'7em'	);
		$('.loadfile-label'	).css( 'top',		'0em'	);
		$('.now_dir'		).css( 'top',		'4.5em'	);
		$('.fld_itm'		).css( 'top',		'30%'	);
		$('.del_fil'		).css( 'top',		'25%'	);

		$('.tbl_hdr'		).css( 'height',	'6em'	);
		$('.tbl_hdr_nme'	).css( 'height',	'3em'	);
		$('.tbl_hdr_ext'	).css( 'height',	'3em'	);
		$('.dir_itm_cnt'	).css( 'height',	'8em'	);
		$('.dir_itm_nme'	).css( 'height',	'4em'	);
		$('.dir_itm_ext'	).css( 'height',	'4em'	);
		$('.dir_hdr'		).css( 'height',	'13em'	);
		$('.hom_dir'		).css( 'height',	'4em'	);
		$('.bck_dir'		).css( 'height',	'4em'	);
		$('.ind_sta'		).css( 'height',	'4em'	);
		$('.loadfile-label'	).css( 'height',	'4em'	);
		$('.now_dir'		).css( 'height',	'2em'	);
		$('.nme'			).css( 'height',	'3.3em'	);
		$('.del_fil'		).css( 'height',	'auto'	);

		$('.tbl_hdr_nme'	).css( 'line-height',	'3em'	);
		$('.tbl_hdr_ext'	).css( 'line-height',	'3em'	);
		$('.dir_itm_cnt'	).css( 'line-height',	'3em'	);
		$('.dir_itm_nme'	).css( 'line-height',	'3em'	);
		$('.dir_itm_ext'	).css( 'line-height',	'3em'	);
		$('.hom_dir'		).css( 'line-height',	'4em'	);
		$('.bck_dir'		).css( 'line-height',	'4em'	);
		$('.bck_dir'		).css( 'line-height',	'4em'	);
		$('.loadfile-label'	).css( 'line-height',	'4em'	);
		$('.ind_sta'		).css( 'line-height',	'4em'	);
		$('.nme'			).css( 'line-height',	'3.3em'	);

		$('.hom_dir'		).css( 'margin',	'0em'	);
		$('.bck_dir'		).css( 'margin',	'0em'	);
		$('.now_dir'		).css( 'margin',	'0em'	);
		$('.ind_sta'		).css( 'margin',	'0em'	);

		$('.dir_itm_nme'	).css( 'font-size',		'200%'	);
		$('.dir_itm_ext'	).css( 'font-size',		'250%'	);
		$('.tbl_hdr_nme'	).css( 'font-size',		'200%'	);
		$('.nme'			).css( 'font-size',		'120%'	);
		$('.tbl_hdr_ext'	).css( 'font-size',		'200%'	);
		$('.hom_dir'		).css( 'font-size',		'200%'	);
		$('.bck_dir'		).css( 'font-size',		'200%'	);
		$('.now_dir'		).css( 'font-size',		'200%'	);
		$('.ind_sta'		).css( 'font-size',		'200%'	);
		$('.loadfile-label'	).css( 'font-size',		'200%'	);

		$('.bck_dir'		).css( 'left',		'22%'	);
		$('.xls_inp_frm'	).css( 'left',		'44%'	);
		$('.ind_sta'		).css( 'left',		'74%'	);
		$('.now_dir'		).css( 'left',		'0em'	);
		$('.nme'			).css( 'left',		'15%'	);

		$('.xls_inp_frm'	).css( 'width',		'28%'	);
		$('.hom_dir'		).css( 'width',		'20%'	);
		$('.bck_dir'		).css( 'width',		'20%'	);
		$('.ind_sta'		).css( 'width',		'29%'	);

		$('.dir_itm_ext'	).css( 'right',		'8%'	);

		$('.now_dir'		).css( 'width',	'103%'	);
		$('.del_fil'		).css( 'width',		'7%'	);
		$('.dir_itm_nme'	).css( 'width',		'79%'	);
		$('.dir_itm_ext'	).css( 'width',		'11%'	);

		$('.nme'			).css( 'max-width',		'89%'	);
	}
	else{
		$('.tbl_bdy'		).attr('style', '');
		$('.scr_bar'		).attr('style', '');
		$('.loadfile-label'	).attr('style', '');
		$('.now_dir'		).attr('style', '');
		$('.fld_itm_ext'	).attr('style', '');
		$('.del_fil'		).attr('style', '');
		$('.tbl_hdr'		).attr('style', '');
		$('.tbl_hdr_nme'	).attr('style', '');
		$('.tbl_hdr_ext'	).attr('style', '');
		$('.dir_itm_cnt'	).attr('style', '');
		$('.dir_itm_nme'	).attr('style', '');
		$('.dir_itm_ext'	).attr('style', '');
		$('.dir_hdr'		).attr('style', '');
		$('.hom_dir'		).attr('style', '');
		$('.bck_dir'		).attr('style', '');
		$('.ind_sta'		).attr('style', '    background-color: rgb(5, 255, 51);');
		$('.nme'			).attr('style', '');
		$('.xls_inp_frm'	).attr('style', '');

	}

	if (phn_ori > 0 ){
		console.log("album");
		$('.dir_itm_ext'	).css( 'right',		'4%'	);
		$('.dir_itm_ext'	).css( 'width',		'6%'	);
		$('.nme'			).css( 'width',		'89%'	);
	}

}

function chk_con(){

	var res;
	$('.ind_sta').css("background-color", "orange");
	$.ajax({
			  type: "POST", 
			  url: "/dir/chk_con",
			  data: {},
			  success: function(data){res = data},
			  dataType: 'json',
			  async: false,
			  timeout: 60,
			});
			// console.log(res);

	if (res == 1){
		$('.ind_sta').css("background-color", "rgb(5 255 51)");
		get_dfl_dir();}
	else{$('.ind_sta').css("background-color", "red");}	
}

function get_dfl_dir(){
	ovr_blk_shw();
	function ctl_exe___xls_upl() {
		var res;
		$('.lst_dir').empty();

		$.ajax({
			  type: "POST", 
			  url: "/dir/get_dfl_dir",
			  data: {},
			  success: function(data){res = data;},
			  dataType: 'json',
			  async: false,
			  timeout: 60,
			});
		// console.log(res.dta);
		dir_lst =  JSON.parse(res).sta;
		shw_dir(dir_lst);

		$('.now_dir').text('/');
		ovr_blk_hde(); 
	}
	setTimeout( ctl_exe___xls_upl, del_tme );
}

function rld_dir(){

	ovr_blk_shw(); 
	function ctl_exe___xls_upl() {

		// dir_cnt = $().closest('.dir_itm_cnt')

		var res;
		// dir_nme = $(dir_cnt).find('.nme').text()
		// dir_ext = $(dir_cnt).find('.dir_itm_ext').text()

		$('.lst_dir').empty();

		now_dir = $('.now_dir').text();
		dta = {"now_dir": now_dir, "dir_nme": ''}

		$.ajax({
			  type: "POST", 
			  url: "/dir/get_dir",
			  data: dta,
			  success: function(data){res = data;},
			  dataType: 'json',
			  async: false,
			  timeout: 600000,
			});
		// console.log(res.dta);

		dta =  JSON.parse(res.dta).sta;
		dir_lst = dta.dir_lst;
		dir_new = dta.dir_new
		if (dir_lst.length > 0){shw_dir(dir_lst);}
		else{}


		adj_hgh()

		ovr_blk_hde(); 
	}
	setTimeout( ctl_exe___xls_upl, del_tme );

}

function get_dir(dir_itm){

	ovr_blk_shw(); 
	function ctl_exe___xls_upl() {

		dir_cnt = $(dir_itm).closest('.dir_itm_cnt')

		var res;
		dir_nme = $(dir_cnt).find('.nme').text()
		dir_ext = $(dir_cnt).find('.dir_itm_ext').text()

		if (dir_ext == 'Folder'){


			$('.lst_dir').empty();

			now_dir = $('.now_dir').text();
			dta = {"now_dir": now_dir, "dir_nme": dir_nme}

			$.ajax({
				  type: "POST", 
				  url: "/dir/get_dir",
				  data: dta,
				  success: function(data){res = data;},
				  dataType: 'json',
				  async: false,
				  timeout: 600000,
				});
			// console.log(res.dta);

			dta =  JSON.parse(res.dta).sta;
			dir_lst = dta.dir_lst;
			dir_new = dta.dir_new
			if (dir_lst.length > 0){shw_dir(dir_lst);}
			else{}

			if(dir_new == ''){dir_new = '/'}
			
			$('.now_dir').text(dir_new);	
		}
		else{
			var res;
			now_dir = $('.now_dir').text();
			dta = {"now_dir": now_dir, "dir_nme": dir_nme, 'ext': dir_ext}

			$.ajax({
				  type: "POST", 
				  url: "/dir/dwn_fil",
				  data: dta,
				  success: function(data){	res = data;  },
				  // dataType: 'json',
				  async: false,
				  timeout: 600000,
				});

			var x=window.open();
			doc_lnk =  JSON.parse(res).dta;
			x.document.location.replace(doc_lnk)
		}
		adj_hgh()

		ovr_blk_hde(); 
	}
	setTimeout( ctl_exe___xls_upl, del_tme );

}

function get_bck_dir(){


	ovr_blk_shw(); 
	function ctl_exe___xls_upl() {


	now_dir = $('.now_dir').text();
	dta = {"now_dir": now_dir}
	$('.lst_dir').empty();
	$.ajax({
		  type: "POST", 
		  url: "/dir/get_dir_bck",
		  data: dta,
		  success: function(data){res = data;},
		  dataType: 'json',
		  async: false,
		  timeout: 600000,
		});
	// console.log(res.dta);
	dta =  JSON.parse(res.dta).sta;
	dir_lst = dta.dir_lst;
	dir_new = dta.dir_new
	shw_dir(dir_lst);
	if(dir_new == ''){dir_new = '/'}
	
	$('.now_dir').text(dir_new);
	adj_hgh()

		ovr_blk_hde(); 
	}
	setTimeout( ctl_exe___xls_upl, del_tme );



}

const delay = async (ms) => await new Promise(resolve => setTimeout(resolve, ms));

function sleep(millis) {
    var t = (new Date()).getTime();
    var i = 0;
    while (((new Date()).getTime() - t) < millis) {
        i++;
    }
}

var tim_arr = []

function shw_dir(dir_lst){

	ovr_blk_shw(); 
	function ctl_exe___xls_upl() {

		del = 10;
		idx = 0;
		tim_arr.forEach(tim_itm => {clearTimeout(tim_itm)});

		dir_lst.forEach(dir_itm => {
			if (dir_itm['ext'] == 'Folder')
			{
				tim_arr.push( setTimeout(function fff(){
					tmp = ''																		+
						'<div class = "dir_itm_cnt">'			+
						'	<div class="dir_itm_nme">'			+
						'		<img class = "fld_itm" src = "static/img/folder_icn.png">'			+
						'		<div class = "nme">' + dir_itm['nme'] + '</div>'		+
						'</div>'																	+
						'	<div class = "dir_itm_ext">' + dir_itm['ext'] + '</div>'			+
						'	<img class = "del_fil" src = "static/img/del_fil_icn.png">'		+
						'</div>';
					$('.lst_dir').append(tmp);
					adj_hgh()
				},del*idx))
				idx = idx + 1;

			}
		});

		dir_lst_srt = _.sortBy(dir_lst, [(o) => o.ext]);

		dir_lst_srt.forEach(dir_itm => {

			if (dir_itm['ext'] != 'Folder')
			{
				tim_arr.push( setTimeout(function fff(){
					pth = 'not_pad.png'
					ext = dir_itm['ext'].toLowerCase();
					if (ext == '.docx'	){pth = 'word.png'		}
					if (ext == '.doc'	){pth = 'word.png'		}
					if (ext == '.xlsx'	){pth = 'excel.png'		}
					if (ext == '.pptx'	){pth = 'powr_pnt.png'	}
					if (ext == '.pdf'	){pth = 'pdf.png'		}
					if (ext == '.jpg'	){pth = 'jpg.png'		}
					if (ext == '.png'	){pth = 'png.png'		}
					if (ext == '.mp4'	){pth = 'mp4.png'		}
					if (ext == '.py'	){pth = 'py.png'		}
					if (ext == '.m'		){pth = 'matlab.png'	}

					tmp = ''																	+
						'<div class = "dir_itm_cnt oncontextmenu="return false;">'		+
						'	<div class="dir_itm_nme">'		+
						'		<img class = "fld_itm" src = "static/img/' + pth + '">'			+
						'		<div class = "nme">' + dir_itm['nme'] + '</div>'	+
						'</div>'																+
						'	<div class = "dir_itm_ext">' + dir_itm['ext'] + '</div>'		+
						'	<img class = "del_fil" src = "static/img/del_fil_icn.png">'		+
						'</div>';
					$('.lst_dir').append(tmp);
					adj_hgh()
					
				},del*idx))
				// setTimeout(function(){fff()}, 20000*idx);
				idx = idx + 1;
			}
		});
		adj_hgh()
		ovr_blk_hde(); 
	}
	setTimeout( ctl_exe___xls_upl, del_tme );
	
}

function del_fil(dir_itm){


	ovr_blk_shw(); 
	function ctl_exe___xls_upl() {

		if (confirm('Удалить?')) {

			dir_cnt = $(dir_itm).closest('.dir_itm_cnt')

			var res;
			dir_nme = $(dir_cnt).find('.nme').text()
			dir_ext = $(dir_cnt).find('.dir_itm_ext').text()

			$('.lst_dir').empty();

			now_dir = $('.now_dir').text();
			dta = {"now_dir": now_dir, "dir_nme": dir_nme}

			$.ajax({
				  type: "POST", 
				  url: "/dir/del_fil",
				  data: dta,
				  success: function(data){res = data;},
				  dataType: 'json',
				  async: false,
				  timeout: 600000,
				});

			dta		=	JSON.parse(res.dta).sta;
			dir_lst	=	dta.dir_lst;
			dir_new	=	dta.dir_new
			if (dir_lst.length > 0){shw_dir(dir_lst);}
			else{}

			if(dir_new == ''){dir_new = '/'}

			$('.now_dir').text(dir_new);	
		}
		else{console.log('no')}

		adj_hgh()

		ovr_blk_hde(); 
	}
	setTimeout( ctl_exe___xls_upl, del_tme );



}

function rnm_sbm(){

	new_nme = $('.rnm_nme_inp')[0].value
	old_nme = $('.met_rnm').text()
	rnm_dir = $('.now_dir').text()
	
	dta = {
		'new_nme': new_nme,
		'old_nme': old_nme,	
		'rnm_dir': rnm_dir
	}


	$.ajax({
		  type: "POST", 
		  url: "/dir/rnm_fil",
		  data: dta,
		  success: function(data){res = data;},
		  dataType: 'json',
		  async: false,
		  timeout: 600000,
		});

	rld_dir();
	$('.rnm_cnt').hide();
	$('.rnm_cnt').removeClass('usr_sel')

}

function ovr_blk_shw() { $( '.gar_cnt'	).css({ 'display': 'block'}); };

function ovr_blk_hde() { $( '.gar_cnt'	).css({ 'display': 'none'});};

function ctl_exe___xls_upl() {  chk_con(); ovr_blk_hde();  }