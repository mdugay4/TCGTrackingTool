function toggle(){
    var demo= document.querySelector(".demo")
    var video= document.querySelector(".video")
    demo.classList.toggle("active");
    video.pause();
    video.currentTime = 0;
}

$('img.close').click(function(){
	$('.youtube-video')[0].contentWindow.postMessage('{"event":"command","func":"' + 'stopVideo' + '","args":""}', '*');
});
