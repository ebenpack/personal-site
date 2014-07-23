Title: Wireframe
Slug: projects/wireframe
Tags: JavaScript
Date: 2014-07-22 15:15
Authors: ebenpack
Description: 3D software engine.
Status: hidden


<div class="main" style="position:relative; width: 600px; margin: 80px auto">
    <canvas tabindex="1" id="wireframe" style="background-color:black; position:relative; border: 2px solid green;" width="600" height="400"></canvas>
    <p>Click on the canvas to give it focus. Move with WASDRF keys. Look around with QETG. Spin icosahedron with HJKLUI.</p>
    <div id="controls">
        <button id="toggledraw">Toggle draw mode</button>
        <button id="togglebfcull">Toggle backface culling</button>
    </div>
</div>

<script src="{filename}/js/wireframe.js"></script>
<script src="{filename}/js/wireframe.demo.js"></script>
