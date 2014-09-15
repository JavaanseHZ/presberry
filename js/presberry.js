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

function getSlideIndexNormal()
{
	return $("#presentationWrapper").slickCurrentSlide();
}

function getSlideIndexPreview()
{
	return $("#presentationWrapper").slickCurrentSlide() - 1;
}

function getSlideIndexNotes()
{
	return $("#presentationWrapper").slickCurrentSlide() * 2;
}

$(document).on('pageshow', '#presentationPage', function(){
	if($('#presentationWrapper').getSlick() != undefined)
	{
		$('#presentationWrapper').slickUnfilter();
		$("#presentationWrapper").unslick();
	}
	$.get('/startPresentation', function(data) {
		var mode = data['mode'];
		var order = data['order'];		
		if(order == "normal")
			cbFunction = getSlideIndexNormal;
		else if(order == "preview")
			cbFunction = getSlideIndexPreview;
		else if(order == "notes")
			cbFunction = getSlideIndexNotes;				
		if(mode == "click")
		{
			$("#presentationWrapper").slick({
				lazyLoad: 'ondemand',
				onAfterChange : null
			});
			$('#presentationWrapper').on('click', '.car-slide', function(){
				var pageIndex = cbFunction();
				$.post('/setPage', {pageNr: pageIndex}, function(data) {},'json');				
			});
		}
		else if(mode == "change")
		{
			$("#presentationWrapper").slick({
				lazyLoad: 'ondemand',
				onAfterChange : function(){
					var pageIndex = cbFunction();
					$.post('/setPage', {pageNr: pageIndex}, function(data) {},'json');			
				}
			});
			$('#presentationWrapper').off('click', '.car-slide');
		}
		if(order == "notes")
			$('#presentationWrapper').slickFilter(':odd');
					
	},'json');
	//$.post('/setPage', {pageNr: 0}, function(data) {},'json');
	
	var screen = $.mobile.getScreenHeight();
	var header = $(".ui-header").outerHeight()  - 1;
	var footer = $(".ui-footer").outerHeight() - 1 ;
	var contentCurrent = $(".ui-content").outerHeight() - $(".ui-content").height();
	var content = screen - header - footer - contentCurrent;
	$(".ui-content").height(content);
});

$(document).on('pagehide', '#presentationPage', function(){
	$.get('/quitPresentation', function(data) {},'json');
	
	//$("#presentationWrapper").hide();
});

$("#fullscreenButton").click(function () {
	var target = $( ".ui-page-active" )[0];
    if (screenfull.enabled) {
        screenfull.request(target);
    }
});

//$("#startPresentationButton").click(function () {
//	$(this).hide();
//	$("#presentationWrapper").show();
//});

//$(document).on('pagecreate', '#presentationPage', function(){
//	$(".car-container").slick({
//		
//	});
//});

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
		$("#presentationWrapper").unslick();
		//$("#presentation").hide();
		var presFile = new FormData(this);
		$.ajax({
		    url: '/upload',
		    data: presFile,
		    cache: false,
		    contentType: false,
		    processData: false,
		    type: 'POST',
		    success: function(data){
		    	
		    	$("#presentationWrapper").html(data['html']);
		    	$("#previewUpload").html(data['preview']);
		    }
		}).done(function() {
			alert(data['preview']);
			//$("#previewUpload").html(data['preview']);
			
//				$("#presentationWrapper").slick({
//					lazyLoad: 'ondemand'
//				});
				//$(".car-container").slickAdd(data['html']);
				//alert("done");
			  
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
