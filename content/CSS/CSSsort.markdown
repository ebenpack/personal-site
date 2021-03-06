Title: Sorting with CSS
Tags: HTML, CSS
Slug: css-sort
Date: 2014-08-22 13:52
Authors: ebenpack
Description: Sorting content with pure CSS.
Summary: Sorting content with pure CSS.


Prompted by the following question asked on reddit.com/r/webdev:

> Hello, is it possible to sort something by popularity using only CSS and HTML? Or do i need to use something else like JS etc.?

> - /u/justanewboy

I have devised the following solution:

    #!html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Document</title>
        <style>
            .container {position: relative; height: 200px;}
            .sorted {height:20px; position: absolute;}
            .sorted[data-sort='1']  {top: 0;}
            .sorted[data-sort='2']  {top: 20px;}
            .sorted[data-sort='3']  {top: 40px;}
            .sorted[data-sort='4']  {top: 60px;}
            .sorted[data-sort='5']  {top: 80px;}
            .sorted[data-sort='6']  {top: 100px;}
            .sorted[data-sort='7']  {top: 120px;}
            .sorted[data-sort='8']  {top: 140px;}
            .sorted[data-sort='9']  {top: 160px;}
            .sorted[data-sort='10'] {top: 180px;}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="sorted" data-sort="2">2</div>
            <div class="sorted" data-sort="3">3</div>
            <div class="sorted" data-sort="1">1</div>
            <div class="sorted" data-sort="6">6</div>
            <div class="sorted" data-sort="4">4</div>
            <div class="sorted" data-sort="10">10</div>
            <div class="sorted" data-sort="9">9</div>
            <div class="sorted" data-sort="5">5</div>
            <div class="sorted" data-sort="8">8</div>
            <div class="sorted" data-sort="7">7</div>
        </div>
    </body>
    </html>

Here's an example of it in action.

<div class="container" style="position: relative; height:200px; width:100%;">
    <style scoped>
        .sorted {height: 20px; position: absolute;}
        .sorted[data-sort='1']  {top: 0;}
        .sorted[data-sort='2']  {top: 20px;}
        .sorted[data-sort='3']  {top: 40px;}
        .sorted[data-sort='4']  {top: 60px;}
        .sorted[data-sort='5']  {top: 80px;}
        .sorted[data-sort='6']  {top: 100px;}
        .sorted[data-sort='7']  {top: 120px;}
        .sorted[data-sort='8']  {top: 140px;}
        .sorted[data-sort='9']  {top: 160px;}
        .sorted[data-sort='10'] {top: 180px;}
    </style>
    <div class="sorted" data-sort="2">2</div>
    <div class="sorted" data-sort="3">3</div>
    <div class="sorted" data-sort="1">1</div>
    <div class="sorted" data-sort="6">6</div>
    <div class="sorted" data-sort="4">4</div>
    <div class="sorted" data-sort="10">10</div>
    <div class="sorted" data-sort="9">9</div>
    <div class="sorted" data-sort="5">5</div>
    <div class="sorted" data-sort="8">8</div>
    <div class="sorted" data-sort="7">7</div>
</div>

Have a look at the HTML and you'll see that these items are not represented in the markup in the order that you're seeing them on the page (assuming you're using a modern browser, and you don't have any sort of user stylesheet overriding these rules). Or better yet, try to select the text and see what horrors CSS hath wrought.

Of course it should go without saying that you should almost certainly never, ever do such a thing. But it's still interesting to see what CSS is capable of these days. To put it in bold letters: **CSS sort is nowhere close to cross-browser compatible, and is almost certainly inappropriate for all real-world situations**.

That said, I'm not sure if this could be generalized a bit more (i.e. to obviate the repetition of `.sorted[data-sort='x'] {top:(20*x)px;}`), but I'll be sure to edit this post with any new results I discover. I'm also curious about the time complexity of such a sorting algorithm. Intuition tells me it's likely to be something like O(n*log(selector)<sup>property</sup>). Don't quote me on that, though.

And finally, I apologize if this is old news. I couldn't find any references to anything similar to this, but I would not be surprised if this isn't a new discovery. If you know of prior art, let me know by submitting an issue on [github](https://github.com/ebenpack/ebenpack.github.io/issues).
