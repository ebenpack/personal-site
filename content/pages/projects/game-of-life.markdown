Title: Conway's Game of Life
Slug: pages/projects/game-of-life
Tags: JavaScript
Date: 2014-02-15 20:28
Authors: ebenpack
Description: Conway's Game of Life made with JavaScript.
Status: hidden

<div id="game" class="game">
    <canvas id="gol" style="border: 1px solid black;position:relative;" width='600' height='400'></canvas>
</div>
<script src="{filename}/js/bundle.js"></script>
<script>
(function(){
    var GOL = new main.conway('gol', 50);
})();
</script>
