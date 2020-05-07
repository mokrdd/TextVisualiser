$(function () {
    $(document).on("click", ".process_button", function () {
        var val = $("#value").val();
        var url = window.location.href + "process"

        $.ajax({
            type: "GET",
            url: url,
            headers: {
                "Content-Type": "text/plain",
                "HTTP_GROUP_NAME": "groups_name",
            },
            data: {
                "val": val
            },
            success: function (res) {
                console.log(res.result);
                console.log("called");
                draw(res.result);
                console.log("finished");

                //arr = res.result;
                //elems = 0;
                //curr_elem = "input_window"
                //arr.forEach((element) => {
                //    console.log(element);
                //    elem_id = "jstree_demo_div_" + elems++;
                //    str = "<div class=\"" + elem_id + " tree\"></div>";
                //    $("." + curr_elem).after(str)
                //    $("."+elem_id).jstree({
                //        'core': {
                //            //'data': [{ "id": "\u0432\u044b\u0434\u0430\u0451\u0442\u0441\u044f", "parent": "#", "text": "\u0432\u044b\u0434\u0430\u0451\u0442\u0441\u044f", "opened": "true" }, { "id": "\u041a\u0430\u0436\u0434\u043e\u043c\u0443", "parent": "\u043f\u043e\u0441\u0435\u0442\u0438\u0442\u0435\u043b\u044e", "text": "\u041a\u0430\u0436\u0434\u043e\u043c\u0443", "opened": "true" }, { "id": "\u043f\u043e\u0441\u0435\u0442\u0438\u0442\u0435\u043b\u044e", "parent": "\u0432\u044b\u0434\u0430\u0451\u0442\u0441\u044f", "text": "\u043f\u043e\u0441\u0435\u0442\u0438\u0442\u0435\u043b\u044e", "opened": "true" }, { "id": "\u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438", "parent": "\u043f\u043e\u0441\u0435\u0442\u0438\u0442\u0435\u043b\u044e", "text": "\u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438" }, { "id": "\u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0430", "parent": "\u0432\u044b\u0434\u0430\u0451\u0442\u0441\u044f", "text": "\u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0430" }, { "id": ".", "parent": "\u043a\u0430\u0440\u0442\u043e\u0447\u043a\u0430", "text": "." }]
                //            'data': element
                //        }
                //    });
                //    curr_elem = elem_id
                //})
                
                //alert(res);
            }  
        });
    }); 
});

var $container = $('.input_container');
var $backdrop = $('.input_backdrop');
var $highlights = $('.highlights');
var $textarea = $('textarea');
var $toggle = $('button');

// yeah, browser sniffing sucks, but there are browser-specific quirks to handle that are not a matter of feature detection
var ua = window.navigator.userAgent.toLowerCase();
var isIE = !!ua.match(/msie|trident\/7|edge/);
var isWinPhone = ua.indexOf('windows phone') !== -1;
var isIOS = !isWinPhone && !!ua.match(/ipad|iphone|ipod/);

function applyHighlights(text) {
    console.log("applyHighlights("+text+")");
    text = text
        .replace(/\n$/g, '\n\n')
        .replace(/[A-Z].*?\b/g, '<mark>$&</mark>');

    if (isIE) {
        // IE wraps whitespace differently in a div vs textarea, this fixes it
        text = text.replace(/ /g, ' <wbr>');
    }

    return text;
}

function handleInput() {
    console.log("handleInput(");
    var text = $textarea.val();
    var highlightedText = applyHighlights(text);
    $highlights.html(highlightedText);
}

function handleScroll() {
    console.log("handleScroll");
    var scrollTop = $textarea.scrollTop();
    $backdrop.scrollTop(scrollTop);

    var scrollLeft = $textarea.scrollLeft();
    $backdrop.scrollLeft(scrollLeft);
}

function fixIOS() {
    // iOS adds 3px of (unremovable) padding to the left and right of a textarea, so adjust highlights div to match
    $highlights.css({
        'padding-left': '+=3px',
        'padding-right': '+=3px'
    });
}

function bindEvents() {
    console.log("handleScroll");
    $textarea.on({
        'input': handleInput,
        'scroll': handleScroll
    });
}

if (isIOS) {
    fixIOS();
}

bindEvents();
handleInput();