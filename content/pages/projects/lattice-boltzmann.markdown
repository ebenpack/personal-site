Title: Lattice Boltzmann
Slug: projects/lattice-boltzmann
Tags: JavaScript
Date: 2014-02-15 20:28
Authors: ebenpack
Status: hidden

<div class="main" style="position:relative;">
    <canvas id="boltzmann" style="background-color: black;" width='600' height='240'></canvas>
    <canvas id="vectorcanvas" style="position: absolute; left: 0; top: 0; pointer-events: none" width='600' height='240'></canvas>
    <canvas id="particlecanvas" style="position: absolute; left: 0; top: 0; pointer-events: none" width='600' height='240'></canvas>
    <canvas id="barriercanvas" style="position: absolute; left: 0; top: 0; pointer-events: none" width='600' height='240'></canvas>
     <div id="controls" class="controls">
        <select id="drawmode">
            <option value="speed">Speed</option>
            <option value="xvelocity">X Velocity</option>
            <option value="yvelocity">Y Velocity</option>
            <option value="density">Density</option>
            <option value="curl">Curl</option>
            <option value="nothing">Nothing</option>
        </select>
        <label><input id="flowvectors" type="checkbox" name="flowvectors"> Flow Vectors</label>
        <label><input id="flowparticles" type="checkbox" name="flowparticles"> Flow Particles</label>
        <button id="play">Start</button>
        <button id="reset">Reset</button>
        <button id="clearbarriers">Clear barriers</button>
        <br>
        <br>
        <label><input id="viscosity" type="range" name="viscosity" min="2" max="50"> Viscosity</label><br><br>
        <label><input id="speed" type="range" name="anim-speed" min="1" max="15"> Animation Speed</label>
    </div>
    <div style="border:1px solid gray; width: 600px; padding: 10px; margin-top:10px;">
        <p><b>Left click</b> to drag fluid</p>
        <p><b>Right click</b> to draw/erase barriers</p>
    </div>
    <div id="debug"></div>
</div>
<script src="https://rawgithub.com/ebenpack/laboratory/master/JS/boltzmann/js/init.js"></script>
<script src="https://rawgithub.com/ebenpack/laboratory/master/JS/boltzmann/js/draw.js"></script>
<script src="https://rawgithub.com/ebenpack/laboratory/master/JS/boltzmann/js/events.js"></script>
<script src="https://rawgithub.com/ebenpack/laboratory/master/JS/boltzmann/js/main.js"></script>