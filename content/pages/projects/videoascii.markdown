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

<script src="{filename}/js/videoascii.js"></script>
<script>
     (function(){
        var canvas = document.getElementById('canvas');
        var ctx = canvas.getContext('2d');
        var video = document.createElement('video');

        // Prepare canvas and display instruction
        canvas.style.border = "4px dashed gray";
        ctx.textAlign="center"; 
        ctx.font="14pt Arial"; 
        ctx.fillText("Drop video files here to asciify", 150, 150); 

        function make_ascii(canvas, video){
            // canvas.width = video.width;
            // canvas.height = video.height;
            canvas.style.border = "";
            videoascii({
                canvas: canvas,
                video: video,
                font_size: 8,
                monochrome: false,
                autoplay: true
            });

        }

        // Register canvas drag 'n' drop handler
        canvas.addEventListener("dragover", function (e) {
            e.preventDefault();
        }, false);
        canvas.addEventListener("drop", function (e) {
            var files = e.dataTransfer.files;
            if (files.length > 0) {
                var file = files[0];
                if (typeof FileReader !== "undefined" && file.type.indexOf("video") != -1) {
                    var reader = new FileReader();
                    reader.onload = function (evt) {
                        video.src = evt.target.result;
                        make_ascii(canvas, video);
                    };
                reader.readAsDataURL(file);
                }
            }
            e.preventDefault();
        }, false);  
    })()
</script>
