Title: JS1K Lattice Boltzmann
Slug: pages/projects/js1k
Tags: JavaScript
Date: 2014-02-15 20:28
Authors: ebenpack
Description: An implementation of the lattice Boltzmann method with JavaScript for the JS1k contest.
Status: hidden

<canvas id="c" style="position: relative;"></canvas>
<script>
  var a = document.getElementsByTagName('canvas')[0];
  var b = document.body;
  var c = a.getContext('2d');
  a.width = a.height = 600;
</script>
<script src="{filename}/js/wavybits.js"></script>