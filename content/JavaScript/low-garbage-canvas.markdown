Title: A Load of Garbage
Tags: JavaScript, Canvas
Slug: low-garbage-canvas
Date: 2014-08-28 9:30
Authors: ebenpack
Description: A few thoughts on writing low garbage JavaScript apps for the canvas.
Summary: A few thoughts on writing low garbage JavaScript apps for the canvas.

After I completed a working version of my 3D rendering engine [wireframe.js]({filename}/pages/projects/wireframe.markdown), I started looking for ways to make improvements, both in terms of performance, and usability. While both efforts are still ongoing, there are a few things I have learned with regard to performance that I wanted to get down in writing.

One of the main areas of focus for performance on this project has been memory management. In order to achieve a smooth, stable 60 frames per second, you have just under 17ms to complete all of the operations required to get a frame on the screen. This includes any physics or game logic you might need to execute, as well as the time required to paint the frame itself. I don't know if you've heard, but 17ms is not very much time at all. So when a garbage collection (GC) event occurs, this takes some time away from the already tight 17ms you have to draw your frame. And if you don't have those extra milliseconds to spare for a GC event (and you don't really have much say in when they occur, so you can't exactly plan for them), this can result in skipped frames, which can appear to the user as a stutter or pause. I believe some folks call it jank.

So how do we avoid this? Well, the obvious answer is: if you want to avoid garbage collection, then don't make so much garbage. It may sound an easy thing, but the details of just how to achieve this can be a little more tricky. First, just where does garbage come from in JavaScript? If you aren't experienced with memory management, the answer may not be obvious.

Simply put, creating a new object requires the interpreter to allocate memory for that object. But isn't everything in JavaScript an object? Well... yes and no. Strings, numbers, and booleans (so long as they aren't instantiated by their respective `String`, `Number` or `Boolean` constructors) and `null` and `undefined` are all primitive types, meaning they're not, strictly speaking, objects. They do, however, behave like objects on occasion. When a method is called on a primitive type, a wrapper object is quickly created for that value in order to call the method, and then, just as quickly, it is discarded. And, more importantly, while they may not technically be objects, they still need some memory allocated in order to store them.

Garbage is what happens to the memory allocated to objects that are no longer in use (or, more specifically, objects that are no longer referenced). Once an object is no longer referenced in a program, the interpreter can mark this object as garbage that needs to be collected (i.e. memory which can be deallocated). E.g.:

    #!javascript
    // Memory allocated for first array object.
    var foo = [1,2,3,4,5,6];

    // foo assigned to second array object. Memory allocated
    // for second array object. First array object
    // no longer referenced, can be marked for GC.
    foo = ['a', 'b', 'c'];

    // bar assigned to value of foo. Second array object now
    // referenced by both foo and bar.
    var bar = foo;
    
    // foo assigned to 'bar', but second array still
    // referenced by bar, so cannot be marked for GC.
    foo = 'bar';

But while virtually anything you do in JavaScript will require the allocation of some amount of memory, the situation is not so hopeless as it may seem. After all, the goal is to reduce garbage, not necessarily to reduce the total amount of memory allocated (although memory use should always be kept as low as possible). As garbage is created when an object is no longer referenced, there are a few strategies to reduce garbage collection.

What it boils down to is that, in order to reduce garbage, it is imperative that, as much as possible, you should not discard objects once they have been created. wireframe.js provides us with a good case study of how this can be achieved in a project that makes use of the canvas, and for JavaScript in general.

In the first, 'high-garbage' iteration, I was using a version of the [linearalgea.js](https://github.com/ebenpack/linearalgea.js) math library (which I created especially to perform the matrix and vector math required by a 3D rendering engine) that created and returned a new matrix, or a new vector, for virtually every method call. As a general design decision, this mostly made sense. You want your matrices and vectors to be more or less immutable. You don't want the methods you're calling to change the value of the object itself, as you often need to use these matrices and vectors in multiple operations. E.g.:

    #!javascript
    // Old, high-garbage methods
    Vector.prototype.subtract = function(vector){
        return new Vector(
            this.x - vector.x,
            this.y - vector.y,
            this.z - vector.z
        );
    };
    Vector.prototype.cross = function(vector){
        return new Vector(
            (this.y * vector.z) - (this.z * vector.y),
            (this.z * vector.x) - (this.x * vector.z),
            (this.x * vector.y) - (this.y * vector.x)
        );
    };

    // Three vertices of a triangle
    var vertex1 = new Vector(1,2,3);
    var vertex2 = new Vector(4,5,6);
    var vertex3 = new Vector(7,8,9);

    // Find vectors representing two sides of the triangle
    // We may still need to use the vertices later,
    // so an in-place operation would not be appropriate
    var side1 = vertex2.subtract(vertex1);
    var side2 = vertex3.subtract(vertex1);

    // Find the normal of the triangle, using the two sides
    var normal = side1.cross(side2);

The above code does what we want, but it also creates three new vectors along the way. Assume we run this code just once per frame (in reality it will run many times per frame, potentially once per triangle of every mesh in our scene). This means that for every frame, we are adding three new vectors as garbage that will need to be collected (assuming the interpreter isn't smart enough to make some reuse of them, which... are there any interpreters that do that? I don't know).

The solution to this problem was to add 'low-garbage' versions of all of these methods which do not create a new vector or matrix, but which rather assign the result of the operation to a matrix or vector object that is passed to the method call. As JavaScript uses a call-by-sharing evaluation strategy (which means that mutations made to a mutable argument inside a function  will be visible outside of that function), we can pass an object to a function that we will use to store the results of the function call.

This method of returning results might be familiar to those of you who are have some experience with C. In C, functions are limited in what they can return; e.g. a function cannot return an array. Instead, a function can return a pointer to an array, or, alternatively, a pointer to the array can be assigned to a pointer that is passed as an argument to the function.

The above example, rewritten to use the low-garbage methods, would look something like this:

    #!javascript
    // New, low-grabage methods
    Vector.prototype.subtractLG = function(vector, result){
        result.x = this.x - vector.x;
        result.y = this.y - vector.y;
        result.z = this.z - vector.z;
    };
    Vector.prototype.crossLG = function(vector, result){
        result.x = (this.y * vector.z) - (this.z * vector.y);
        result.y = (this.z * vector.x) - (this.x * vector.z);
        result.z = (this.x * vector.y) - (this.y * vector.x);
    };

    // Results vectors
    var side1 = new Vector(0,0,0);
    var side12 = new Vector(0,0,0);
    var normal = new Vector(0,0,0);

    // Three vertices of a triangle
    var vertex1 = new Vector(1,2,3);
    var vertex2 = new Vector(4,5,6);
    var vertex3 = new Vector(7,8,9);

    // Find vectors representing two sides of the triangle
    vertex2.subtractLG(vertex1, side1);
    vertex3.subtractLG(vertex1, side2);

    // Find the normal of the triangle, using the two sides
    side1.crossLG(side2, normal);

This example may look very similar to the earlier example. And if it was executed as-is, since the results vectors would be created anew for every frame, there would be little or no difference between this and the earlier version in terms of memory use. The key difference comes when these results vectors are created just once, and a reference is kept in order to prevent them from being garbage collected. So now, instead of creating and discarding a new object for every method call, multiple times per frame, we're creating just a handful of objects upon initialization, and using them over and over.

Implementing low-garbage versions of all of the matrix and vector methods had a fairly large impact for wireframe.js. Compare the before and after graphs below.

<svg viewbox="0 0 835 120">
    <g transform="translate(0,50)">
        <path class="chartfill" d="M0,-22L4.2,0L8.4,0L12.6,0L16.8,-6L21,-6L25.2,-6L29.400000000000002,18L33.6,18L37.8,10L42,10L46.2,10L50.4,4L54.6,4L58.800000000000004,-4.0000000000000036L63,-4.0000000000000036L67.2,-10L71.4,14L75.6,14L79.8,5.999999999999998L84,5.999999999999998L88.2,0L92.4,0L96.60000000000001,-8.000000000000004L100.8,16L105,16L109.2,16L113.4,10L117.60000000000001,10L121.8,10L126,2L130.2,2L134.4,-4.0000000000000036L138.6,-4.0000000000000036L142.8,-4.0000000000000036L147,-12L151.2,-12L155.4,-12L159.6,12L163.8,4L168,4L172.20000000000002,4L176.4,-2L180.6,-10L184.8,-10L189,14L193.20000000000002,7.999999999999998L197.4,7.999999999999998L201.6,7.999999999999998L205.79999999999998,0L210,-6L214.20000000000002,-6L218.4,-12L222.60000000000002,18L226.8,10L231.00000000000003,10L235.20000000000002,4L239.40000000000003,4L243.6,4L247.79999999999998,-4.0000000000000036L252,-10L256.2,-10L260.4,-12L264.6,14L268.8,5.999999999999998L273,5.999999999999998L277.2,5.999999999999998L281.40000000000003,5.999999999999998L285.6,0L289.8,0L294,-8.000000000000004L298.2,-8.000000000000004L302.4,-8.000000000000004L306.59999999999997,16L310.8,16L315,10L319.2,10L323.40000000000003,2L327.6,-4.0000000000000036L331.8,-4.0000000000000036L336,-12L340.20000000000005,-12L344.40000000000003,12L348.6,12L352.8,5.999999999999998L357,-2L361.2,-2L365.4,-8.000000000000004L369.6,-8.000000000000004L373.8,14L378,14L382.2,7.999999999999998L386.40000000000003,7.999999999999998L390.6,0L394.8,-6L399,-6L403.2,18L407.4,18L411.59999999999997,10L415.8,10L420,4L424.2,-4.0000000000000036L428.40000000000003,-10L432.6,-10L436.8,14L441,14L445.20000000000005,5.999999999999998L449.40000000000003,0L453.6,0L457.8,-8.000000000000004L462.00000000000006,-8.000000000000004L466.20000000000005,-8.000000000000004L470.40000000000003,16L474.6,16L478.80000000000007,10L483.00000000000006,10L487.2,2L491.4,2L495.59999999999997,-4.0000000000000036L499.79999999999995,-4.0000000000000036L504,-12L508.2,12L512.4,12L516.6,5.999999999999998L520.8,5.999999999999998L525,-2L529.2,-2L533.4,-8.000000000000004L537.6,-8.000000000000004L541.8000000000001,16L546,16L550.2,7.999999999999998L554.4,7.999999999999998L558.6,2L562.8000000000001,-6L567,-6L571.2,18L575.4000000000001,18L579.6,10L583.8000000000001,10L588,4L592.1999999999999,4L596.4,4L600.6,-4.0000000000000036L604.8,-4.0000000000000036L609,-4.0000000000000036L613.1999999999999,-10L617.4,-10L621.6,14L625.8,14L630,5.999999999999998L634.2,5.999999999999998L638.4,0L642.6,-8.000000000000004L646.8000000000001,-8.000000000000004L651,16L655.2,10L659.4,10L663.6,2L667.8000000000001,2L672,-4.0000000000000036L676.2,-12L680.4000000000001,-12L684.6,12L688.8000000000001,12L693,5.999999999999998L697.2,5.999999999999998L701.4,-2L705.6,-8.000000000000004L709.8,16L714,16L718.1999999999999,16L722.4,7.999999999999998L726.6,7.999999999999998L730.8,2L735,-6L739.2,-12L743.4,18L747.6,10L751.8000000000001,10L756,10L760.2,4L764.4,-4.0000000000000036L768.6,-4.0000000000000036L772.8000000000001,-4.0000000000000036L777,-10L781.2,-10L785.4000000000001,14L789.6,14L793.8000000000001,5.999999999999998L798,5.999999999999998L802.2,0L806.4,0L810.6,-8.000000000000004L814.8,-8.000000000000004L819,-12L823.1999999999999,16L827.4,10L831.6,10L835.8,2L835.8,25L0,25L0,-22"></path>
        <path class="chartline" d="M0,-22L4.2,0L8.4,0L12.6,0L16.8,-6L21,-6L25.2,-6L29.400000000000002,18L33.6,18L37.8,10L42,10L46.2,10L50.4,4L54.6,4L58.800000000000004,-4.0000000000000036L63,-4.0000000000000036L67.2,-10L71.4,14L75.6,14L79.8,5.999999999999998L84,5.999999999999998L88.2,0L92.4,0L96.60000000000001,-8.000000000000004L100.8,16L105,16L109.2,16L113.4,10L117.60000000000001,10L121.8,10L126,2L130.2,2L134.4,-4.0000000000000036L138.6,-4.0000000000000036L142.8,-4.0000000000000036L147,-12L151.2,-12L155.4,-12L159.6,12L163.8,4L168,4L172.20000000000002,4L176.4,-2L180.6,-10L184.8,-10L189,14L193.20000000000002,7.999999999999998L197.4,7.999999999999998L201.6,7.999999999999998L205.79999999999998,0L210,-6L214.20000000000002,-6L218.4,-12L222.60000000000002,18L226.8,10L231.00000000000003,10L235.20000000000002,4L239.40000000000003,4L243.6,4L247.79999999999998,-4.0000000000000036L252,-10L256.2,-10L260.4,-12L264.6,14L268.8,5.999999999999998L273,5.999999999999998L277.2,5.999999999999998L281.40000000000003,5.999999999999998L285.6,0L289.8,0L294,-8.000000000000004L298.2,-8.000000000000004L302.4,-8.000000000000004L306.59999999999997,16L310.8,16L315,10L319.2,10L323.40000000000003,2L327.6,-4.0000000000000036L331.8,-4.0000000000000036L336,-12L340.20000000000005,-12L344.40000000000003,12L348.6,12L352.8,5.999999999999998L357,-2L361.2,-2L365.4,-8.000000000000004L369.6,-8.000000000000004L373.8,14L378,14L382.2,7.999999999999998L386.40000000000003,7.999999999999998L390.6,0L394.8,-6L399,-6L403.2,18L407.4,18L411.59999999999997,10L415.8,10L420,4L424.2,-4.0000000000000036L428.40000000000003,-10L432.6,-10L436.8,14L441,14L445.20000000000005,5.999999999999998L449.40000000000003,0L453.6,0L457.8,-8.000000000000004L462.00000000000006,-8.000000000000004L466.20000000000005,-8.000000000000004L470.40000000000003,16L474.6,16L478.80000000000007,10L483.00000000000006,10L487.2,2L491.4,2L495.59999999999997,-4.0000000000000036L499.79999999999995,-4.0000000000000036L504,-12L508.2,12L512.4,12L516.6,5.999999999999998L520.8,5.999999999999998L525,-2L529.2,-2L533.4,-8.000000000000004L537.6,-8.000000000000004L541.8000000000001,16L546,16L550.2,7.999999999999998L554.4,7.999999999999998L558.6,2L562.8000000000001,-6L567,-6L571.2,18L575.4000000000001,18L579.6,10L583.8000000000001,10L588,4L592.1999999999999,4L596.4,4L600.6,-4.0000000000000036L604.8,-4.0000000000000036L609,-4.0000000000000036L613.1999999999999,-10L617.4,-10L621.6,14L625.8,14L630,5.999999999999998L634.2,5.999999999999998L638.4,0L642.6,-8.000000000000004L646.8000000000001,-8.000000000000004L651,16L655.2,10L659.4,10L663.6,2L667.8000000000001,2L672,-4.0000000000000036L676.2,-12L680.4000000000001,-12L684.6,12L688.8000000000001,12L693,5.999999999999998L697.2,5.999999999999998L701.4,-2L705.6,-8.000000000000004L709.8,16L714,16L718.1999999999999,16L722.4,7.999999999999998L726.6,7.999999999999998L730.8,2L735,-6L739.2,-12L743.4,18L747.6,10L751.8000000000001,10L756,10L760.2,4L764.4,-4.0000000000000036L768.6,-4.0000000000000036L772.8000000000001,-4.0000000000000036L777,-10L781.2,-10L785.4000000000001,14L789.6,14L793.8000000000001,5.999999999999998L798,5.999999999999998L802.2,0L806.4,0L810.6,-8.000000000000004L814.8,-8.000000000000004L819,-12L823.1999999999999,16L827.4,10L831.6,10L835.8,2"></path>
        <line x1="0" y1="25" x2="835" y2="25" style="stroke: #8F8F8F;"/>
        <text x="2" y="45" font-family="Verdana" font-size="15" style="fill:#8F8F8F;">5.7MB-9.7MB</text>
    </g>
</svg>
<div class="illustration-label">Memory usage for 'high-garbage' math methods</div>


<svg viewbox="0 0 835 120">
    <g transform="translate(0,50)">
        <path class="chartfill" d="M0,-22L4.2,14L8.4,14L12.6,12L16.8,12L21,7.999999999999998L25.2,7.999999999999998L29.400000000000002,5.999999999999998L33.6,4L37.8,4L42,0L46.2,0L50.4,-2L54.6,-2L58.800000000000004,-6L63,-6L67.2,-8.000000000000004L71.4,-8.000000000000004L75.6,-12L79.8,-12L84,18L88.2,18L92.4,14L96.60000000000001,14L100.8,12L105,12L109.2,7.999999999999998L113.4,5.999999999999998L117.60000000000001,5.999999999999998L121.8,2L126,2L130.2,0L134.4,0L138.6,-2L142.8,-2L147,-6L151.2,-6L155.4,-8.000000000000004L159.6,-8.000000000000004L163.8,-12L168,-12L172.20000000000002,18L176.4,18L180.6,14L184.8,14L189,12L193.20000000000002,7.999999999999998L197.4,7.999999999999998L201.6,5.999999999999998L205.79999999999998,5.999999999999998L210,2L214.20000000000002,2L218.4,0L222.60000000000002,0L226.8,-4.0000000000000036L231.00000000000003,-4.0000000000000036L235.20000000000002,-6L239.40000000000003,-6L243.6,-8.000000000000004L247.79999999999998,-8.000000000000004L252,-8.000000000000004L256.2,-12L260.4,-12L264.6,16L268.8,16L273,14L277.2,12L281.40000000000003,12L285.6,7.999999999999998L289.8,7.999999999999998L294,5.999999999999998L298.2,5.999999999999998L302.4,2L306.59999999999997,2L310.8,0L315,0L319.2,-4.0000000000000036L323.40000000000003,-4.0000000000000036L327.6,-6L331.8,-6L336,-8.000000000000004L340.20000000000005,-8.000000000000004L344.40000000000003,-12L348.6,-12L352.8,16L357,16L361.2,14L365.4,14L369.6,10L373.8,10L378,7.999999999999998L382.2,7.999999999999998L386.40000000000003,5.999999999999998L390.6,5.999999999999998L394.8,2L399,2L403.2,0L407.4,0L411.59999999999997,-4.0000000000000036L415.8,-4.0000000000000036L420,-4.0000000000000036L424.2,-6L428.40000000000003,-6L432.6,-6L436.8,-10L441,-10L445.20000000000005,-12L449.40000000000003,-12L453.6,-14L457.8,16L462.00000000000006,14L466.20000000000005,14L470.40000000000003,14L474.6,10L478.80000000000007,10L483.00000000000006,7.999999999999998L487.2,7.999999999999998L491.4,7.999999999999998L495.59999999999997,4L499.79999999999995,4L504,2L508.2,0L512.4,0L516.6,-4.0000000000000036L520.8,-4.0000000000000036L525,-4.0000000000000036L529.2,-6L533.4,-10L537.6,-10L541.8000000000001,-12L546,-12L550.2,16L554.4,14L558.6,14L562.8000000000001,10L567,10L571.2,7.999999999999998L575.4000000000001,7.999999999999998L579.6,7.999999999999998L583.8000000000001,4L588,4L592.1999999999999,2L596.4,2L600.6,-2L604.8,-2L609,-4.0000000000000036L613.1999999999999,-4.0000000000000036L617.4,-6L621.6,-6L625.8,-10L630,-10L634.2,-12L638.4,-12L642.6,16L646.8000000000001,16L651,12L655.2,12L659.4,10L663.6,10L667.8000000000001,7.999999999999998L672,7.999999999999998L676.2,4L680.4000000000001,2L684.6,2L688.8000000000001,-2L693,-2L697.2,-2L701.4,-4.0000000000000036L705.6,-8.000000000000004L709.8,-8.000000000000004L714,-10L718.1999999999999,-10L722.4,-12L726.6,-12L730.8,16L735,16L739.2,12L743.4,12L747.6,12L751.8000000000001,10L756,7.999999999999998L760.2,7.999999999999998L764.4,4L768.6,4L772.8000000000001,2L777,2L781.2,2L785.4000000000001,-2L789.6,-4.0000000000000036L793.8000000000001,-4.0000000000000036L798,-8.000000000000004L802.2,-8.000000000000004L806.4,-8.000000000000004L810.6,-10L814.8,-10L819,-14L823.1999999999999,-14L827.4,16L831.6,16L835.8,12L835.8,25L0,25L0,-22"></path>
        <path class="chartline" d="M0,-22L4.2,14L8.4,14L12.6,12L16.8,12L21,7.999999999999998L25.2,7.999999999999998L29.400000000000002,5.999999999999998L33.6,4L37.8,4L42,0L46.2,0L50.4,-2L54.6,-2L58.800000000000004,-6L63,-6L67.2,-8.000000000000004L71.4,-8.000000000000004L75.6,-12L79.8,-12L84,18L88.2,18L92.4,14L96.60000000000001,14L100.8,12L105,12L109.2,7.999999999999998L113.4,5.999999999999998L117.60000000000001,5.999999999999998L121.8,2L126,2L130.2,0L134.4,0L138.6,-2L142.8,-2L147,-6L151.2,-6L155.4,-8.000000000000004L159.6,-8.000000000000004L163.8,-12L168,-12L172.20000000000002,18L176.4,18L180.6,14L184.8,14L189,12L193.20000000000002,7.999999999999998L197.4,7.999999999999998L201.6,5.999999999999998L205.79999999999998,5.999999999999998L210,2L214.20000000000002,2L218.4,0L222.60000000000002,0L226.8,-4.0000000000000036L231.00000000000003,-4.0000000000000036L235.20000000000002,-6L239.40000000000003,-6L243.6,-8.000000000000004L247.79999999999998,-8.000000000000004L252,-8.000000000000004L256.2,-12L260.4,-12L264.6,16L268.8,16L273,14L277.2,12L281.40000000000003,12L285.6,7.999999999999998L289.8,7.999999999999998L294,5.999999999999998L298.2,5.999999999999998L302.4,2L306.59999999999997,2L310.8,0L315,0L319.2,-4.0000000000000036L323.40000000000003,-4.0000000000000036L327.6,-6L331.8,-6L336,-8.000000000000004L340.20000000000005,-8.000000000000004L344.40000000000003,-12L348.6,-12L352.8,16L357,16L361.2,14L365.4,14L369.6,10L373.8,10L378,7.999999999999998L382.2,7.999999999999998L386.40000000000003,5.999999999999998L390.6,5.999999999999998L394.8,2L399,2L403.2,0L407.4,0L411.59999999999997,-4.0000000000000036L415.8,-4.0000000000000036L420,-4.0000000000000036L424.2,-6L428.40000000000003,-6L432.6,-6L436.8,-10L441,-10L445.20000000000005,-12L449.40000000000003,-12L453.6,-14L457.8,16L462.00000000000006,14L466.20000000000005,14L470.40000000000003,14L474.6,10L478.80000000000007,10L483.00000000000006,7.999999999999998L487.2,7.999999999999998L491.4,7.999999999999998L495.59999999999997,4L499.79999999999995,4L504,2L508.2,0L512.4,0L516.6,-4.0000000000000036L520.8,-4.0000000000000036L525,-4.0000000000000036L529.2,-6L533.4,-10L537.6,-10L541.8000000000001,-12L546,-12L550.2,16L554.4,14L558.6,14L562.8000000000001,10L567,10L571.2,7.999999999999998L575.4000000000001,7.999999999999998L579.6,7.999999999999998L583.8000000000001,4L588,4L592.1999999999999,2L596.4,2L600.6,-2L604.8,-2L609,-4.0000000000000036L613.1999999999999,-4.0000000000000036L617.4,-6L621.6,-6L625.8,-10L630,-10L634.2,-12L638.4,-12L642.6,16L646.8000000000001,16L651,12L655.2,12L659.4,10L663.6,10L667.8000000000001,7.999999999999998L672,7.999999999999998L676.2,4L680.4000000000001,2L684.6,2L688.8000000000001,-2L693,-2L697.2,-2L701.4,-4.0000000000000036L705.6,-8.000000000000004L709.8,-8.000000000000004L714,-10L718.1999999999999,-10L722.4,-12L726.6,-12L730.8,16L735,16L739.2,12L743.4,12L747.6,12L751.8000000000001,10L756,7.999999999999998L760.2,7.999999999999998L764.4,4L768.6,4L772.8000000000001,2L777,2L781.2,2L785.4000000000001,-2L789.6,-4.0000000000000036L793.8000000000001,-4.0000000000000036L798,-8.000000000000004L802.2,-8.000000000000004L806.4,-8.000000000000004L810.6,-10L814.8,-10L819,-14L823.1999999999999,-14L827.4,16L831.6,16L835.8,12"></path>
        <line x1="0" y1="25" x2="835" y2="25" style="stroke: #8F8F8F;"/>
        <text x="2" y="45" font-family="Verdana" font-size="15" style="fill:#8F8F8F;">9.9MB-13.9MB</text>
    </g>
</svg>
<div class="illustration-label">Memory usage for 'low-garbage' math methods</div>

While overall these memory graphs have a similar shape, the latter has a far more regular GC pattern. It grows steadily, and then there's a GC event, which produces the characteristic sawtooth pattern. The 'high-garbage' version, on the other hand, grows some, then has a GC event, grows, grows, GC, etc. Overall the shape is vaguely sawtooth-like, but there are far more GC events that occur sporadically between the trough and the peak of the sawtooth, and the memory graph appears much more erratic.

Depending on what your aims are, in order to fully make use of this sort of approach it may be necessary to implement object pooling. What this means is that you have a 'pool' of objects that you have instantiated. When you need a new object, you pull one from the pool. When you no longer need that object, you return it to the pool. There is a bit more overhead in this, so if you know ahead of time exactly how many objects you will need, and you are certain that you will never need more than this, object pooling would likely not be worth the effort.

It should be noted, though that care must be taken when using this method, whether with an object pool or without, to initialize the results object to ensure that old values from previous calculations are completely removed from your results object. For example, the following matrix translation static method can cause problems if the results matrix still carries values from previous calculations:

    #!javascript
    // If the result matrix still has values in 0-11 or 15 from
    // being used in previous calculations, this will cause problems.
    Matrix.translation = function(xtrans, ytrans, ztrans, result){
        result[12] = xtrans;
        result[13] = ytrans;
        result[14] = ztrans;
    };

The way I have implemented the low-garbage methods in these examples also makes method chaining impossible, but chaining can be achieved by simply explicitly returning the result. This does not have any negative repercussions in terms of memory usage or performance.

Alright, so far, so good. Implementing the low garbage math methods—and refactoring the main 3D rendering function to make use of these methods—had a very noticeable effect on the memory-use profile of the program. Garbage collection was now much less frequent, and at more regular intervals. But garbage can also sneak in where you don't expect it, and there was still work to be done.

The two graphs above represent a ~2 second time slice. So in the 'good' version, GC events are still occurring approximately every 200ms. This could be better, and I was certain that there were still areas of the program that were still making too much garbage. The most obvious place to look was this line, which occurs at the beginning of the render function:

    #!javascript
    back_buffer_img = back_buffer_ctx.createImageData(width, height);

The back buffer is an `ImageData` array (which is a `Uint8ClampedArray`, which is a typed array) where pixel data is written. This image data is then drawn to an offscreen buffer canvas, which is then used to draw to the main canvas. While this may seem like a lot of extra, unnecessary steps, the main advantage of this is that it allows the 3D scene to be initially drawn in one resolution, but displayed in a different resolution. So a scene can be upscaled in order to use fewer resources, or it can be downscaled to provide a better looking image.

As `createImageData` creates a new `ImageData` array, in this early version of the program a new back buffer array was being created for every frame. Naturally, this created a lot of unnecessary garbage. In my first attempt to tackle this problem, I was running over the entire array, zeroing out all the values.

Backing up a little, an `ImageData` array is a one-dimensional array representing the RGBA values of all pixels in a 2D canvas context, with each element representing either a red, green, blue, or alpha value of a pixel. So, for example, a 1x1 pixel `ImageData` array might look like this `[1, 7, 2, 9]`, where the RGBA values are 1, 7, 2, and 9 respectively.

So it should be clear that for any `ImageData` array, its length will be described by canvas width * canvas height * 4. As it turned out, looping over the entire array was actually noticeably slower than just creating a new `ImageData` array for every frame, even with all the extra garbage that brought with it. However, if you consider for a moment what it is we're trying to achieve (clearing the back buffer for the next frame), it may become clear that we can actually get away with doing ¼ of the work. By setting the alpha value to zero, we can ignore the RGB values, just so long as we make sure to set all RGBA values when we draw a new pixel to the array. With this change, each frame took less time to draw (meaning fewer resources were used), and GC events became much less frequent. Here is what memory use looked like after this change (the scale is the same as the previous two graphs):

<svg viewbox="0 0 835 120">
    <g transform="translate(0,50)">
        <path class="chartfill" d="M0,5.999999999999998L4.2,5.999999999999998L8.4,5.999999999999998L12.6,5.999999999999998L16.8,5.999999999999998L21,5.999999999999998L25.2,4L29.400000000000002,4L33.6,4L37.8,4L42,4L46.2,4L50.4,2L54.6,2L58.800000000000004,2L63,2L67.2,2L71.4,2L75.6,0L79.8,0L84,0L88.2,0L92.4,0L96.60000000000001,0L100.8,-2L105,-2L109.2,-2L113.4,-2L117.60000000000001,-2L121.8,-2L126,-2L130.2,-4.0000000000000036L134.4,-4.0000000000000036L138.6,-4.0000000000000036L142.8,-4.0000000000000036L147,-4.0000000000000036L151.2,-6L155.4,-6L159.6,-6L163.8,-6L168,-6L172.20000000000002,-6L176.4,-6L180.6,-8.000000000000004L184.8,-8.000000000000004L189,-8.000000000000004L193.20000000000002,-8.000000000000004L197.4,-8.000000000000004L201.6,-8.000000000000004L205.79999999999998,-8.000000000000004L210,-10L214.20000000000002,-10L218.4,-10L222.60000000000002,-10L226.8,-10L231.00000000000003,-10L235.20000000000002,-10L239.40000000000003,-12L243.6,-12L247.79999999999998,-12L252,-12L256.2,-12L260.4,18L264.6,18L268.8,18L273,18L277.2,16L281.40000000000003,16L285.6,16L289.8,16L294,16L298.2,16L302.4,16L306.59999999999997,14L310.8,14L315,14L319.2,14L323.40000000000003,14L327.6,12L331.8,12L336,12L340.20000000000005,12L344.40000000000003,12L348.6,12L352.8,10L357,10L361.2,10L365.4,10L369.6,10L373.8,10L378,10L382.2,7.999999999999998L386.40000000000003,7.999999999999998L390.6,7.999999999999998L394.8,7.999999999999998L399,7.999999999999998L403.2,5.999999999999998L407.4,5.999999999999998L411.59999999999997,5.999999999999998L415.8,5.999999999999998L420,5.999999999999998L424.2,5.999999999999998L428.40000000000003,5.999999999999998L432.6,4L436.8,4L441,4L445.20000000000005,4L449.40000000000003,4L453.6,4L457.8,4L462.00000000000006,2L466.20000000000005,2L470.40000000000003,2L474.6,2L478.80000000000007,2L483.00000000000006,2L487.2,0L491.4,0L495.59999999999997,0L499.79999999999995,0L504,0L508.2,0L512.4,0L516.6,-2L520.8,-2L525,-2L529.2,-2L533.4,-2L537.6,-2L541.8000000000001,-4.0000000000000036L546,-4.0000000000000036L550.2,-4.0000000000000036L554.4,-4.0000000000000036L558.6,-4.0000000000000036L562.8000000000001,-4.0000000000000036L567,-4.0000000000000036L571.2,-6L575.4000000000001,-6L579.6,-6L583.8000000000001,-6L588,-6L592.1999999999999,-8.000000000000004L596.4,-8.000000000000004L600.6,-8.000000000000004L604.8,-8.000000000000004L609,-8.000000000000004L613.1999999999999,-8.000000000000004L617.4,-8.000000000000004L621.6,-10L625.8,-10L630,-10L634.2,-10L638.4,-10L642.6,-10L646.8000000000001,-12L651,-12L655.2,-12L659.4,18L663.6,18L667.8000000000001,18L672,18L676.2,16L680.4000000000001,16L684.6,16L688.8000000000001,16L693,16L697.2,16L701.4,14L705.6,14L709.8,14L714,14L718.1999999999999,14L722.4,14L726.6,14L730.8,14L735,12L739.2,12L743.4,12L747.6,12L751.8000000000001,12L756,12L760.2,12L764.4,10L768.6,10L772.8000000000001,10L777,10L781.2,10L785.4000000000001,10L789.6,10L793.8000000000001,7.999999999999998L798,7.999999999999998L802.2,7.999999999999998L806.4,7.999999999999998L810.6,7.999999999999998L814.8,5.999999999999998L819,5.999999999999998L823.1999999999999,5.999999999999998L827.4,5.999999999999998L831.6,5.999999999999998L835.8,5.999999999999998L835.8,25L0,25L0,5.999999999999998"></path>
        <path class="chartline" d="M0,5.999999999999998L4.2,5.999999999999998L8.4,5.999999999999998L12.6,5.999999999999998L16.8,5.999999999999998L21,5.999999999999998L25.2,4L29.400000000000002,4L33.6,4L37.8,4L42,4L46.2,4L50.4,2L54.6,2L58.800000000000004,2L63,2L67.2,2L71.4,2L75.6,0L79.8,0L84,0L88.2,0L92.4,0L96.60000000000001,0L100.8,-2L105,-2L109.2,-2L113.4,-2L117.60000000000001,-2L121.8,-2L126,-2L130.2,-4.0000000000000036L134.4,-4.0000000000000036L138.6,-4.0000000000000036L142.8,-4.0000000000000036L147,-4.0000000000000036L151.2,-6L155.4,-6L159.6,-6L163.8,-6L168,-6L172.20000000000002,-6L176.4,-6L180.6,-8.000000000000004L184.8,-8.000000000000004L189,-8.000000000000004L193.20000000000002,-8.000000000000004L197.4,-8.000000000000004L201.6,-8.000000000000004L205.79999999999998,-8.000000000000004L210,-10L214.20000000000002,-10L218.4,-10L222.60000000000002,-10L226.8,-10L231.00000000000003,-10L235.20000000000002,-10L239.40000000000003,-12L243.6,-12L247.79999999999998,-12L252,-12L256.2,-12L260.4,18L264.6,18L268.8,18L273,18L277.2,16L281.40000000000003,16L285.6,16L289.8,16L294,16L298.2,16L302.4,16L306.59999999999997,14L310.8,14L315,14L319.2,14L323.40000000000003,14L327.6,12L331.8,12L336,12L340.20000000000005,12L344.40000000000003,12L348.6,12L352.8,10L357,10L361.2,10L365.4,10L369.6,10L373.8,10L378,10L382.2,7.999999999999998L386.40000000000003,7.999999999999998L390.6,7.999999999999998L394.8,7.999999999999998L399,7.999999999999998L403.2,5.999999999999998L407.4,5.999999999999998L411.59999999999997,5.999999999999998L415.8,5.999999999999998L420,5.999999999999998L424.2,5.999999999999998L428.40000000000003,5.999999999999998L432.6,4L436.8,4L441,4L445.20000000000005,4L449.40000000000003,4L453.6,4L457.8,4L462.00000000000006,2L466.20000000000005,2L470.40000000000003,2L474.6,2L478.80000000000007,2L483.00000000000006,2L487.2,0L491.4,0L495.59999999999997,0L499.79999999999995,0L504,0L508.2,0L512.4,0L516.6,-2L520.8,-2L525,-2L529.2,-2L533.4,-2L537.6,-2L541.8000000000001,-4.0000000000000036L546,-4.0000000000000036L550.2,-4.0000000000000036L554.4,-4.0000000000000036L558.6,-4.0000000000000036L562.8000000000001,-4.0000000000000036L567,-4.0000000000000036L571.2,-6L575.4000000000001,-6L579.6,-6L583.8000000000001,-6L588,-6L592.1999999999999,-8.000000000000004L596.4,-8.000000000000004L600.6,-8.000000000000004L604.8,-8.000000000000004L609,-8.000000000000004L613.1999999999999,-8.000000000000004L617.4,-8.000000000000004L621.6,-10L625.8,-10L630,-10L634.2,-10L638.4,-10L642.6,-10L646.8000000000001,-12L651,-12L655.2,-12L659.4,18L663.6,18L667.8000000000001,18L672,18L676.2,16L680.4000000000001,16L684.6,16L688.8000000000001,16L693,16L697.2,16L701.4,14L705.6,14L709.8,14L714,14L718.1999999999999,14L722.4,14L726.6,14L730.8,14L735,12L739.2,12L743.4,12L747.6,12L751.8000000000001,12L756,12L760.2,12L764.4,10L768.6,10L772.8000000000001,10L777,10L781.2,10L785.4000000000001,10L789.6,10L793.8000000000001,7.999999999999998L798,7.999999999999998L802.2,7.999999999999998L806.4,7.999999999999998L810.6,7.999999999999998L814.8,5.999999999999998L819,5.999999999999998L823.1999999999999,5.999999999999998L827.4,5.999999999999998L831.6,5.999999999999998L835.8,5.999999999999998"></path>
        <line x1="0" y1="25" x2="835" y2="25" style="stroke: #8F8F8F;"/>
        <text x="2" y="45" font-family="Verdana" font-size="15" style="fill:#8F8F8F;">4.6MB-6.6MB</text>
    </g>
</svg>
<div class="illustration-label">Memory usage using back buffer zeroing</div>

GC events are now happening about once a second. Which can certainly still be improved upon, but it's miles ahead of where it was to begin with.

As a side note: it occurs to me that in order to clear the back buffer, it would be possible to do potentially much less work than mentioned above. If we kept track of which pixels had been drawn in the previous frame, we could then clear only those pixels which needed clearing. But I suspect that the increased overhead and complexity of such an approach would ultimately not be worthwhile. I will leave it as an exercise to the reader to determine the feasibility of this approach.