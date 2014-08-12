Title: Conway's Game of Life
Slug: projects/game-of-life
Tags: JavaScript
Date: 2014-02-15 20:28
Authors: ebenpack
Description: Conway's Game of Life made with JavaScript.
Status: hidden

<div id="game" class="game">
    <canvas id="gol" style="border: 1px solid black;" width='600px' height='400px'></canvas>
</div>
<script src="{filename}/js/gameoflife.js"></script>
<script>
(function(){
    var GOL = new GameOfLife('gol', 50);
})();
</script>