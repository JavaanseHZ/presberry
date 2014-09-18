var presTimer = new Tock({
	  countdown: false,
	  interval: 1000,
	  callback: function () {
		    var current_time = presTimer.msToTime(presTimer.lap());
		    $('#presentationTimer').text(current_time);
		}
	});

var timerRun = false;

$(document).on('pageshow', '#presentationPage', function(){
	loadPresentation(false);	
});

$(document).on('pagehide', '#presentationPage', function(){
	$.get('/quitPresentation', function(data) {},'json');
	$("#presentationHeader").css({ opacity: 0.9 });
	presTimer.stop();
	presTimer.reset();
	$("#presentationTimer").text("00:00");
	timerRun = false;
});

$(function(){
	$(".fullscreenButton").on('tap', function (e) {
		var target = $.mobile.pageContainer.pagecontainer( "getActivePage" )[0];
	    if (screenfull.enabled) {
	        screenfull.request(target);        
	    }
	});
});

//$( window ).on( "orientationchange", function( event ) {
//	if(screenfull.isFullscreen)
//		loadPresentation(true);
//	else
//		loadPresentation(false);
//});

$(document).on(screenfull.raw.fullscreenchange, function (e) {
	if(screenfull.isFullscreen)
		$(".fullscreenButton").hide();
	else
		$(".fullscreenButton").show();
});

$("#presentationTimer").on('tap', function(e){
	e.preventDefault();
	if(timerRun)
	{
		presTimer.pause();		
	}
	else
	{
		presTimer.start();
		timerRun = true;
	}	
});

$("#presentationTitle").on('tap', function(){
	
	if ($("#presentationHeader").css("opacity").valueOf() > 0.2)
	{
		$("#presentationHeader").css({ opacity: 0.1 });
		$("#presentationFooter").hide();
	}
	else
	{
		$("#presentationHeader").css({ opacity: 0.9 });
		$("#presentationFooter").show();
	}
});

$("[name=slideMode]").change(function(){
	var postdata = $("#settingsForm").serializeArray();
	$.post('/setSettings', postdata, function(data) {},'json');
});

$("[name=slideOrder]").change(function(){
	var postdata = $("#settingsForm").serializeArray();
	$.post('/setSettings', postdata, function(data) {},'json');
});

$("[name=slideTimer]").change(function(){
	var postdata = $("#settingsForm").serializeArray();
	$.post('/setSettings', postdata, function(data) {},'json');
});

$(document).on('pageshow', '#settingsPage', function(){
	$.get('/getSettings', function(data) {
		$( 'input:radio[name="slideMode"]' ).prop( 'checked', false ).checkboxradio( 'refresh' );
		$( 'input:radio[name="slideOrder"]' ).prop( 'checked', false ).checkboxradio( 'refresh' );
		$( 'input:radio[name="slideTimer"]' ).prop( 'checked', false ).checkboxradio( 'refresh' );
		$( 'input:radio[name="slideMode"]' )
			.filter( '[value="' + data['mode'] + '"]' )
			.prop( 'checked', true )
			.checkboxradio( 'refresh' );
		$( 'input:radio[name="slideOrder"]' )
			.filter( '[value="' + data['order'] + '"]' )
			.prop( 'checked', true )
			.checkboxradio( 'refresh' );
		$( 'input:radio[name="slideTimer"]' )
			.filter( '[value="' + data['timer'] + '"]' )
			.prop( 'checked', true )
			.checkboxradio( 'refresh' );
		},'json');
		$('#settingsPage').on('change', 'input', function(){
			e.preventDefault();		
			var postdata = $("#settingsForm").serializeArray();
			$.post('/setSettings', postdata, function(data) {},'json');			
		});	
});

$(document).on('pagecreate', '#uploadPage', function(){
	$("#uploadForm").submit(function(e){
		e.preventDefault();
		$.mobile.loading( "show", {
			  text: "uploading file...",
			  textVisible: true,
			  theme: "b",
			  html: ""
			});
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
		    	$.mobile.loading( "hide");		    	
		    }
		})
	});
	$("#fileList").on('tap', ".presFileItem", function(e){		
		e.preventDefault();
		$("#fileList").find("a").removeClass( "ui-btn-active" );
		$(this).parent().find("a").addClass( "ui-btn-active" );
		$.mobile.loading( "show", {
			  text: "loading presentation...",
			  textVisible: true,
			  theme: "b",
			  html: ""
			});
		var fileName = $(this).children(".presFileName:first").text();
		var fileID = $(this).attr('id');
		$.post('/setupPresentation', {filenameHTML:fileName, timestampID:fileID}, function(data) {
			$("#presentationWrapper").html(data['carousel']);
			$.mobile.loading( "hide");
			$.mobile.pageContainer.pagecontainer("change", $("#presentationPage"));
			$("#fileList").find("a").removeClass( "ui-btn-active" );
			$("#presentationTitle").find("a").removeClass( "ui-btn-active" );
		},'json');		
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
	$.get('/startPresentation', function(data) {
		var mode = data['mode'];
		var order = data['order'];	
		var timer = data['timer'];
		
		if(timer == "timerOn")
			$("#presentationTimer").show();
		else
			$("#presentationTimer").hide();
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
	    var header = $(".ui-header").hasClass("ui-header-fixed") ? $(".ui-header").outerHeight() - 1 : $(".ui-header").outerHeight();
	    var footer = $(".ui-footer").hasClass("ui-footer-fixed") ? $(".ui-footer").outerHeight() - 1 : $(".ui-footer").outerHeight();
	    var contentCurrent = $(".ui-content").outerHeight() - $(".ui-content").height();
	    var content = screen - header - footer - contentCurrent;
	    $("presentationContent").css("min-height", content + "px");
	}
}