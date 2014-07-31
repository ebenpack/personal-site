Title: Too Much Recursion!
Tags: JavaScript
Slug: too-much-recursion
Date: 2014-07-30 21:00
Authors: ebenpack
Description: Q&#58; Does mergesort recursion goes too deep for the language to handle? A&#58; No.
Summary: Q&#58; Does mergesort recursion goes too deep for the language to handle? A&#58; No.

I was reading 'Data Structures and Algorithms in JavaScript' by Michael McMillan the other day. While the book as a whole is absolutely riddled with errors, this passage struck me as being particularly egregious.

> It is customary, though not necessary, to implement Mergesort as a recursive algorithm. However, **it is not possible to do so in JavaScript, as the recursion goes too deep for the language to handle**. [emphasis mine]

It is not possible to implement recursive mergesort in JavaScript! Because the recursion goes too deep! What utter nonsense.

To see why this is such a patently absurd claim, we must first establish a few facts. First, what is the stack depth for JavaScript? This isn't something that is defined by the specification, so it's going to be implementation dependent. User josh3736 reported the stack depths of several browsers in his StackOverflow answer [here](http://stackoverflow.com/questions/7826992/browser-javascript-stack-size-limit#7828803). A quick check of the browsers easily available to hand suggests his assessment to be more or less in the right neighborhood. At worst, we have a stack depth of ~1,000 (insert IE6 joke here), and at best it could be as high as ~65,000. The mean seems to be somewhere around ~20,000-30,000.

The next fact we need to establish is how large can a JavaScript array be? This is a lot more straightforward than the stack depth. The ECMA standard clearly defines the maximum length of an array to be 2<sup>32</sup>-1, or 4,294,967,295. Which is just a hair north of 4 billion. That's a very large array.

So, now that we've sorted out our facts, why is McMillan's claim so absurd? To understand that, we need to take a closer look at mergesort. Mergesort is a textbook divide-and-conquer algorithm. It works by splitting an array in half, then calling mergesort recursively on each half until it reaches the base case. Then it merges each half back together such that the result is sorted. For any given array of sufficient size, mergesort will be called twice, Once on the lower half, and once on the upper half. For each of those halves, mergesort will then potentially be called twice again, and so on.

It should be evident that the number of times an array can be divided in half will be log<sub>2</sub>(n). Not coincidentally, this is the maximum recursive depth mergesort will reach. Put another way, mergesort will reach a recursive depth of n when called on an array of length 2<sup>n</sup>. It follows from this that, given our maximum array length, the maximum recursive depth that mergesort can possibly reach is 32 calls deep (maybe 33 if you count the original call). This is nowhere close to reaching even the shallowest possible stack depth.

I quickly knocked up a recursive mergesort implementation (which I am including below) and set it to work sorting ever larger arrays. My implementation (which I'm sure leaves much room for improvement) crapped out after trying to sort an array of 2<sup>25</sup> items. Not because of what Firefox rather endearingly refers to as "too much recursion", but rather because it takes a heck of a lot of work to sort an array with tens of millions of items. Heck, forget sorting, Chrome wouldn't even let me push more than 2<sup>26</sup> items into an array. So, while it's true that mergesort in JavaScript might have some trouble with arrays of 2<sup>25</sup> items, this has nought to do with the depth of recursion or the call stack. And anyway, why are you trying to sort an array with 2<sup>25</sup> items? Why do you even have an array with 2<sup>25</sup> items? Either way, I doubt McMillan had such large arrays in mind when he made his ridiculous claim.

Just as a thought experiment, though, how large would an array actually need to be to reach or exceed the stack depth of, say, IE6? If you recall, IE6 has a stack depth of ~1,000. Let's just call it 1,000 even. As we demonstrated, in order to reach this recursive depth with mergesort, the array would have to have a length of 2<sup>1,000</sup>. In base-10 this is ~10<sup>301</sup>, this translates to a one followed by 301 other numbers. Here's the actual number:

    10715086071862673209484250490600018105614048117055336074437503883703510511249361224931983788156958581275946729175531468251871452856923140435984577574698574803934567774824230985421074605062371141877954182153046474983581941267398767559165543946077062914571196477686542167660429831652624386837205668069376

It's a pretty big number. It's greater than the number of atoms in the universe. In case you were wondering, there are approx. 10<sup>80</sup> atoms in the observable universe. So it's actually much, much, much greater than the number of atoms in the universe. In fact, any description I could attempt to give w/r/t just how much greater than the number of atoms in the universe this number really is, would just be such a colossal understatement that it would only be an affront to large numbers, and indeed to the very concept of largeness in general. Just believe me when I say that it's wowie big.

The point is, there's a good chance you're not going to be reaching the maximum call stack depth with mergesort, even if you really, really believe your array is well above average size. I would actually go so far as to say it is completely impossible to exceed the stack depth with mergesort in JavaScript, assuming you're sorting a standard JavaScript array and you're using a well implemented mergesort function. So there's a good chance that anyone who claims that

> It is not possible to [implement Mergesort as a recursive algorithm] in JavaScript, as the recursion goes too deep for the language to handle.

might not know what they're talking about. Like, at all.

While this certainly is one of the more flagrant errors in the book, it is just one of many. If you're on the fence about getting this book, I would recommend you give it a pass.

Anyway, here's some code:

    #!javascript
    // The array we will be sorting.
    var big_array = [];

    // Build our array with numbers goins in descending order.
    // The array size, max, can be larger, but things slow down 
    // and start to get wonky at about 2^25.
    var max = Math.pow(2, 20);
    for (var i = 0; i < max; i++){
        big_array.push(max - i);
    }

    big_array = mergesort(big_array);

    function merge(a,b){
        var result = [];
        var alen = a.length;
        var blen = b.length;
        while (alen > 0 || blen > 0){
            if (alen > 0 && blen > 0){
                if (a[0] < b[0]){
                    result.push(a.shift());
                    alen -= 1;
                }
                else if (b[0] <= a[0]){
                    result.push(b.shift());
                    blen -= 1;
                }
            }
            else if (alen > 0){
                result.push(a.shift());
                alen -= 1;
            }
            else if (blen > 0){
                result.push(b.shift());
                blen -= 1;
            }
        }
        return result;
    }

    function mergesort(lst){
        var length = lst.length;
        if (length <= 1){
            return lst;
        }
        // split in half
        var q = Math.floor(length/2)
        // recursive sorts
        var left = mergesort(lst.slice(0,q));
        var right = mergesort(lst.slice(q));
        return merge(left, right);
     }