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

$(document).on('pageshow', '#presentationPage', function(){loadPresentation(false);});

$(document).on('pagehide', '#presentationPage', function(){
	$.get('/quitPresentation', function(data) {},'json');
});

$("#fullscreenButton").on('tap', function (e) {
	e.preventDefault();	
	var target = $( ".ui-page-active" )[0];
    if (screenfull.enabled) {
        screenfull.request(target);        
    }
});

$(document).on(screenfull.raw.fullscreenchange, function (e) {
	if(screenfull.isFullscreen)
		loadPresentation(true);
	else
		loadPresentation(false);
});

$(document).on('pagecreate', '#settingsPage', function(){
	$("#settingsForm").submit(function(e){		
		e.preventDefault();		
		var postdata = $("#settingsForm").serializeArray();
		$.post('/settings', postdata, function(data) {},'json');
	});
});

$(document).on('pagecreate', '#uploadPage', function(){
	$("#uploadForm").submit(function(e){		
		e.preventDefault();
		$("#presentationWrapper").unslick();
		var presFileName = new FormData(this);
		$.ajax({
		    url: '/upload',
		    data: presFileName,
		    cache: false,
		    contentType: false,
		    processData: false,
		    type: 'POST',
		    success: function(data){
		    	$("#fileList").prepend(data['fileListItem']);
		    	var control = $("#uploadFileInput");
		    	control.replaceWith( control = control.clone( true ) ) 
		    }
		})
	});
	$("#fileList").on('tap', ".presFileItem", function(e){
		e.preventDefault();
		var fileName = $(this).children(".presFileName:first").text();
		var fileID = $(this).attr('id');
		$.post('/setupPresentation', {filenameHTML:fileName, timestampID:fileID}, function(data) {
			$("#presentationWrapper").html(data['carousel']);
		},'json');
		$("#fileList").find("a").removeClass( "ui-btn-active" );
		$(this).parent().find("a").addClass( "ui-btn-active" );
	});
	$("#fileList").on('tap', ".presFileItemDelete", function(e){
		e.preventDefault();
		var delFileName = $(this).text();
		var delFileID = $(this).attr('id');
		$.post('/deletePresentation', {filenameHTML:delFileName, delTimestampID:delFileID}, function(data) {
				var fileListItem = "#" + data['delFileID'];
				$(fileListItem).parent().remove();
			},
			'json');		
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

function loadPresentation(fullscreen)
{

	if($('#presentationWrapper').getSlick() != undefined)
	{
		$('#presentationWrapper').slickUnfilter();
		$("#presentationWrapper").unslick();
	}
	
	$(".ui-content").height(content);
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
			$('#presentationWrapper').on('tap', '.car-slide', function(){
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
			$('#presentationWrapper').off('tap', '.car-slide');
		}
		if(order == "notes")
			$('#presentationWrapper').slickFilter(':odd');
					
	},'json');
	if(fullscreen)
	{
		var content = $.mobile.getScreenHeight();
	}
	else
	{
		var screen = $.mobile.getScreenHeight();
		var header = $(".ui-header").outerHeight() - 1;
		var footer = $(".ui-footer").outerHeight() - 1 ;
		var contentCurrent = $(".ui-content").outerHeight() - $(".ui-content").height();
		var content = screen - header - footer - contentCurrent;
		$(".ui-content").height(content);
	}
}