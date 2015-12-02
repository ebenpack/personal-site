Title: A*
Slug: pages/projects/a-star
Tags: JavaScript
Date: 2014-02-15 20:28
Authors: ebenpack
Description: A* pathfinding made with JavaScript.
Status: hidden

<div class="main" style="position:relative;">
    <canvas id="map" style="background-color: black;" width='600' height='240'></canvas>
    <canvas id="particles" style="position: absolute; left: 0; top:0;" width='600' height='240'></canvas>
</div>
<script src="{filename}/js/bundle.js"></script>
<script>
    (function(){
        var maze = new main.astar("map", "particles");
    })();
</script>