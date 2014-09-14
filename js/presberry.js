$(function() {
    $( "[data-role='navbar']" ).navbar();
    $( "[data-role='header'], [data-role='footer']" ).toolbar();
});
$( document ).on( "pagecontainerchange", function() {
    var current = $( ".ui-page-active" ).jqmData( "title" );
    if (current === "Presentation") {
    	$("#fullscreenButton").show();    	
	} else {
		$("#fullscreenButton").hide();
    }
    $( "[data-role='header'] h1" ).text( current );
    $( "[data-role='navbar'] a.ui-btn-active" ).removeClass( "ui-btn-active" );
    $( "[data-role='navbar'] a" ).each(function() {
        if ( $( this ).text() === current ) {
            $( this ).addClass( "ui-btn-active" );
        }
    });
});

$(document).on('pageshow', '#presentationPage', function(){
	var screen = $.mobile.getScreenHeight();

	var header = $(".ui-header").hasClass("ui-header-fixed") ? $(".ui-header").outerHeight()  - 1 : $(".ui-header").outerHeight();

	var footer = $(".ui-footer").hasClass("ui-footer-fixed") ? $(".ui-footer").outerHeight() - 1 : $(".ui-footer").outerHeight();

	var contentCurrent = $(".ui-content").outerHeight() - $(".ui-content").height();

	var content = screen - header - footer - contentCurrent;

	$(".ui-content").height(content);
	$(".car-container").slick({
		onAfterChange:	function() {			
			var pageIndex = $('.slides').slickCurrentSlide();
			$.post('/settings', {pageNr: pageIndex} , function(data) {},'json');
		}
    });
});

$("#fullscreenButton").click(function () {
	var target = $( ".ui-page-active" )[0];
    if (screenfull.enabled) {
        screenfull.request(target);
    }
});

$(document).on('pagecreate', '#settingsPage', function(){
	$("#settingsForm").submit(function(e){		
		e.preventDefault();		
		var postdata = $("#settingsForm").serializeArray();//{slideMode:$("#name").val(), slideOrder: $("#name").val()};
		$.post('/settings', postdata, function(data) {},'json');
	});
});

$(document).on('pagecreate', '#uploadPage', function(){
	$("#uploadForm").submit(function(e){		
		e.preventDefault();
		var presFile = new FormData(this);
		alert("hallo");
		$.ajax({
		    url: '/upload',
		    data: presFile,
		    cache: false,
		    contentType: false,
		    processData: false,
		    type: 'POST',
		    success: function(data){
		        alert(data);
		    }
		});
	});
});



//$(document).on("pagecreate","#presentationPage",function(){
//	var mySwiper = new Swiper('.swiper-container',{
//	mode : 'horizontal',
//	loop : true,
//	watchActiveIndex : true
//	});
//});  
//jQuery( "#presentationPage" ).on( "pagecreate", function( event ) {
//	alert('hallo');
//	var mySwiper = new Swiper('.swiper-container',{
//		mode : 'horizontal',
//		loop : true,
//		watchActiveIndex : true
//		}
//	});
//	var target = $('#presentation')[0];
//	$('#fullscreen').click(function () {
//	    if (screenfull.enabled) {
//	        screenfull.request(target);
//	    }
//	});
//});
