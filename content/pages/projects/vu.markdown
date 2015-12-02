Title: VU
Slug: pages/projects/vu
Tags: JavaScript
Date: 2014-07-29 17:18
Authors: ebenpack
Description: A 3d sound visualizer.
Status: hidden

<canvas id="canvas" width="600" height="400" style="background-color:black;"></canvas>
<div>
    <p>Drop an audio file onto the canvas above (some <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Supported_media_formats">filetype restrictions</a> may apply). You can also use the audio file that is loaded by default. Once the status reads 'Ready!', click the canvas to begin playback.</p>
</div>
<div>
    <p>Click on the canvas to give it focus. Move with WASDRF keys. Look around with QETG.</p>
</div>

<script src="{filename}/js/bundle.js"></script>
<script>
    main.vu();
</script>
