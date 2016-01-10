Title: Lispish
Slug: pages/projects/lispish
Tags: JavaScript
Date: 2014-12-10 18:46
Authors: ebenpack
Description: Some lisp-like noodlings in JS, by someone who doesn't really know lisp.
Status: hidden

   
<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.9/ace.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.9/ext-language_tools.js"></script>
<div style="font-size:16px;">
    <pre style="border:1px solid gray;height:500px;overflow-y: auto;margin-bottom: 5px;" id="input" contentEditable="true">list.reduce(
list.map(
    list.filter(
        list.range(10),
        function(curr){return curr % 2 === 0;}
    ),
    function(curr){return curr * 2;}
),
function(a,b){return a + b;}
);
//=>
cons.print(
list.reverse(
    list.sort(list.list(7,89,5,8,43,2,6,1))
),
{prefix: '', suffix: '', separator: ','}
);
//=>
function add(){
return list.reduce(
    list.list(helpers.args(arguments)),
    function(prev, curr){return curr + prev;}
);
}
fun.curry(add, 5)(1)(2)(3)(4)(5);
//=></pre>
    <div style="-webkit-columns: 3 auto;-moz-columns: 3 auto;columns: 3 auto;border:1px solid gray;height:500px;overflow-y: auto;" id="ref"></div>
    <div style="clear:both; margin:1em;">
        <p>Ctrl-Enter / Cmd-Enter will print results to the special comment //=>. This comment will print the results of the prior statement.</p>
    </div>
</div>
<script src="{filename}/js/bundle.js"></script>
<script>
main.initLispish('input', 'ref');
</script>