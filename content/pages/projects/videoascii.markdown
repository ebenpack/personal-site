Title: VideoASCII
Slug: pages/projects/videoascii
Tags: JavaScript
Date: 2015-11-22 15:19
Authors: ebenpack
Description: An ASCII video renderer.
Status: hidden

<canvas id="canvas" width="300" height="300">
    Sorry, this browser does not support canvas.
</canvas>
<button id="start">Start</button><button id="pause">Pause</button><button id="restart">Restart</button>

<script src="{filename}/js/bundle.js"></script>
<script>
    (function(){
        var canvas = document.getElementById('canvas');
        var start = document.getElementById('start');
        var pause = document.getElementById('pause');
        var restart = document.getElementById('restart');
        var ctx = canvas.getContext('2d');

        // Prepare canvas and display instruction
        canvas.style.border = "4px dashed gray";
        ctx.textAlign = "center"; 
        ctx.font = "14pt Arial"; 
        ctx.fillText("Drop video files here to asciify", 150, 150); 

        function make_ascii(canvas, videoSrc){
            canvas.style.border = "";
            var videoascii = main.videoascii({
                canvas: canvas,
                output_width: canvas.parentElement.offsetWidth,
                videoSrc: videoSrc,
                font_size: 8,
                monochrome: false,
                autoplay: false
            });
            start.addEventListener('click', function(){
                videoascii.start();
            });
            pause.addEventListener('click', function(){
                videoascii.pause();
            });
            restart.addEventListener('click', function(){
                videoascii.restart();
            });
            window.addEventListener('resize', function() {
                videoascii.resize(canvas.parentElement.offsetWidth);
            });
        }

        // Register canvas drag 'n' drop handler
        canvas.addEventListener("dragover", function (e) {
            e.preventDefault();
        }, false);
        canvas.addEventListener("drop", function (e) {
            var files = e.dataTransfer.files;
            var tempvid = document.createElement('video');
            if (files.length > 0) {
                var file = files[0];
                if (tempvid.canPlayType(file.type)) {
                    make_ascii(canvas, file);
                }
            }
            e.preventDefault();
        }, false);  
    })()
</script>