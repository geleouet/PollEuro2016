


var formSave = {
    fields: {}
    , init: function (obj) {
        formSave.that = obj; // storing form object
        // init fields with value and validation function
        $.each(formSave.that.serializeArray(), function (i, field) {
            formSave.fields[field.name] = {
                value: field.value
            };
        });
        formSave.that.submit(formSave.submit); // submit form handler
    }
    , submit: function (e) {
        e.preventDefault();

        var values = {};
        for (var v in formSave.fields) {
            values[v] = formSave.fields[v].value;
            if (v.indexOf('radio') != -1) {
                values[v] = $('input[name='+v+']:checked').val();
            }
            else if (document.getElementById(v))
                values[v] = document.getElementById(v).value

        }
        console.log(values)
        $.post(save_url, values, formSave.success, 'json').error(formSave.error); // making ajax post
    }
    , display_error: function (e, error) {
        var $dd = $('#id_' + e).parent().next('dd'); // get dd error field
        var $error_list = $('<ul/>', {
            'class': 'errorlist'
        }); // create error list
        var $error_em = $('<li/>', {
            html: error
        }); // create error element
        $error_em.appendTo($error_list); // append error element to error list
        $dd.append($error_list); // append error list to dd error field
    }
    , success: function (data, textStatus, jqXHR) {
        if (data['success']) {
            if (typeof afterlogin != 'undefined') {
                window.location.href = afterlogin;
            }
            else {
                location.reload();
            }
        }
    }
    , error: function (jqXHR, textStatus, errorThrown) {
        alert('error: ' + textStatus + errorThrown);
    }
};


var form = {
    fields: {}
    , init: function (obj) {
        form.that = obj; // storing form object
        // init fields with value and validation function
        $.each(form.that.serializeArray(), function (i, field) {
            form.fields[field.name] = {
                value: field.value
            };
        });
        form.that.submit(form.submit); // submit form handler
    }
    , submit: function (e) {
        e.preventDefault();

        var values = {};
        for (var v in form.fields) {
            values[v] = form.fields[v].value;
            if (document.getElementById(v))
                values[v] = document.getElementById(v).value

        }
        $.post(contact_url, values, form.success, 'json').error(form.error); // making ajax post
    }
    , display_error: function (e, error) {
        var $dd = $('#id_' + e).parent().next('dd'); // get dd error field
        var $error_list = $('<ul/>', {
            'class': 'errorlist'
        }); // create error list
        var $error_em = $('<li/>', {
            html: error
        }); // create error element
        $error_em.appendTo($error_list); // append error element to error list
        $dd.append($error_list); // append error list to dd error field
    }
    , success: function (data, textStatus, jqXHR) {
        if (!data['success']) {
            /*form.that.find('dl dd:last-child').empty(); // empty old error messages
            var errors = data;
            for (var e in errors) { // iterating over errors
                var error = errors[e][0];
                form.display_error(e, error);
            }*/

            $('.log-status').addClass('wrong-entry');
            $('.log-btn').addClass('wrong-entry');
            console.log(data['reason']);
            document.getElementById('log-btn').textContent = data['reason'];
            $('.alert').fadeIn(500);
            setTimeout("$('.alert').fadeOut(1500);", 3000);
        } else {
            if (typeof afterlogin != 'undefined') {
                window.location.href = afterlogin;
            }
            else {
                location.reload();
            }
        }
    }
    , error: function (jqXHR, textStatus, errorThrown) {
        alert('error: ' + textStatus + errorThrown);
    }
};



function validateRegister() {
    var x = document.forms["register"]["password"].value;
    var x2 = document.forms["register"]["password2"].value;

    console.log(x)
    console.log(x2)
    if (x == null || x == "" || x != x2) {
        $('.log-status').addClass('wrong-entry');
        $('.log-btn').addClass('wrong-entry');

        document.getElementById('register-btn').textContent = "Passwords must be the same";
        $('.alert').fadeIn(500);
        setTimeout("$('.alert').fadeOut(1500);", 3000);
        return false;
    }
}

$(function () {
    form.init($('#login')); // initialize form
    formSave.init($('#saveP')); // initialize form
});



$(document).ready(function () {




    $('.form-control').keypress(function () {
        $('.log-status').removeClass('wrong-entry');
        $('.log-btn').removeClass('wrong-entry');
        if (document.getElementById('log-btn'))
            document.getElementById('log-btn').textContent = 'Log in';
        if (document.getElementById('register-btn'))
            document.getElementById('register-btn').textContent = 'Register';
    });

    $('.entry').on('change', function () {
        $('.popup').removeClass('hidden')


    });

    $('.popup').addClass('hidden')

    $('#classement').dynatable();
    var dynatable = $('#classement').data('dynatable');
    if (dynatable) {
        dynatable.paginationPerPage.set(20); // Show 20 records per page
        dynatable.process();
    }



});


!function(e,n,t){function r(e,n){return typeof e===n}function s(){var e,n,t,s,o,i,a;for(var l in C)if(C.hasOwnProperty(l)){if(e=[],n=C[l],n.name&&(e.push(n.name.toLowerCase()),n.options&&n.options.aliases&&n.options.aliases.length))for(t=0;t<n.options.aliases.length;t++)e.push(n.options.aliases[t].toLowerCase());for(s=r(n.fn,"function")?n.fn():n.fn,o=0;o<e.length;o++)i=e[o],a=i.split("."),1===a.length?Modernizr[a[0]]=s:(!Modernizr[a[0]]||Modernizr[a[0]]instanceof Boolean||(Modernizr[a[0]]=new Boolean(Modernizr[a[0]])),Modernizr[a[0]][a[1]]=s),g.push((s?"":"no-")+a.join("-"))}}function o(e){var n=w.className,t=Modernizr._config.classPrefix||"";if(_&&(n=n.baseVal),Modernizr._config.enableJSClass){var r=new RegExp("(^|\\s)"+t+"no-js(\\s|$)");n=n.replace(r,"$1"+t+"js$2")}Modernizr._config.enableClasses&&(n+=" "+t+e.join(" "+t),_?w.className.baseVal=n:w.className=n)}function i(){return"function"!=typeof n.createElement?n.createElement(arguments[0]):_?n.createElementNS.call(n,"http://www.w3.org/2000/svg",arguments[0]):n.createElement.apply(n,arguments)}function a(e,n){return!!~(""+e).indexOf(n)}function l(e){return e.replace(/([a-z])-([a-z])/g,function(e,n,t){return n+t.toUpperCase()}).replace(/^-/,"")}function f(e,n){return function(){return e.apply(n,arguments)}}function u(e,n,t){var s;for(var o in e)if(e[o]in n)return t===!1?e[o]:(s=n[e[o]],r(s,"function")?f(s,t||n):s);return!1}function p(e){return e.replace(/([A-Z])/g,function(e,n){return"-"+n.toLowerCase()}).replace(/^ms-/,"-ms-")}function d(){var e=n.body;return e||(e=i(_?"svg":"body"),e.fake=!0),e}function c(e,t,r,s){var o,a,l,f,u="modernizr",p=i("div"),c=d();if(parseInt(r,10))for(;r--;)l=i("div"),l.id=s?s[r]:u+(r+1),p.appendChild(l);return o=i("style"),o.type="text/css",o.id="s"+u,(c.fake?c:p).appendChild(o),c.appendChild(p),o.styleSheet?o.styleSheet.cssText=e:o.appendChild(n.createTextNode(e)),p.id=u,c.fake&&(c.style.background="",c.style.overflow="hidden",f=w.style.overflow,w.style.overflow="hidden",w.appendChild(c)),a=t(p,e),c.fake?(c.parentNode.removeChild(c),w.style.overflow=f,w.offsetHeight):p.parentNode.removeChild(p),!!a}function m(n,r){var s=n.length;if("CSS"in e&&"supports"in e.CSS){for(;s--;)if(e.CSS.supports(p(n[s]),r))return!0;return!1}if("CSSSupportsRule"in e){for(var o=[];s--;)o.push("("+p(n[s])+":"+r+")");return o=o.join(" or "),c("@supports ("+o+") { #modernizr { position: absolute; } }",function(e){return"absolute"==getComputedStyle(e,null).position})}return t}function h(e,n,s,o){function f(){p&&(delete j.style,delete j.modElem)}if(o=r(o,"undefined")?!1:o,!r(s,"undefined")){var u=m(e,s);if(!r(u,"undefined"))return u}for(var p,d,c,h,v,y=["modernizr","tspan","samp"];!j.style&&y.length;)p=!0,j.modElem=i(y.shift()),j.style=j.modElem.style;for(c=e.length,d=0;c>d;d++)if(h=e[d],v=j.style[h],a(h,"-")&&(h=l(h)),j.style[h]!==t){if(o||r(s,"undefined"))return f(),"pfx"==n?h:!0;try{j.style[h]=s}catch(g){}if(j.style[h]!=v)return f(),"pfx"==n?h:!0}return f(),!1}function v(e,n,t,s,o){var i=e.charAt(0).toUpperCase()+e.slice(1),a=(e+" "+E.join(i+" ")+i).split(" ");return r(n,"string")||r(n,"undefined")?h(a,n,s,o):(a=(e+" "+T.join(i+" ")+i).split(" "),u(a,n,t))}function y(e,n,r){return v(e,t,t,n,r)}var g=[],C=[],S={_version:"3.3.1",_config:{classPrefix:"",enableClasses:!0,enableJSClass:!0,usePrefixes:!0},_q:[],on:function(e,n){var t=this;setTimeout(function(){n(t[e])},0)},addTest:function(e,n,t){C.push({name:e,fn:n,options:t})},addAsyncTest:function(e){C.push({name:null,fn:e})}},Modernizr=function(){};Modernizr.prototype=S,Modernizr=new Modernizr;var w=n.documentElement,_="svg"===w.nodeName.toLowerCase(),x=S._config.usePrefixes?" -webkit- -moz- -o- -ms- ".split(" "):["",""];S._prefixes=x;var b="CSS"in e&&"supports"in e.CSS,P="supportsCSS"in e;Modernizr.addTest("supports",b||P);var z="Moz O ms Webkit",E=S._config.usePrefixes?z.split(" "):[];S._cssomPrefixes=E;var T=S._config.usePrefixes?z.toLowerCase().split(" "):[];S._domPrefixes=T;var N={elem:i("modernizr")};Modernizr._q.push(function(){delete N.elem});var j={style:N.elem.style};Modernizr._q.unshift(function(){delete j.style}),S.testAllProps=v,S.testAllProps=y,Modernizr.addTest("cssfilters",function(){if(Modernizr.supports)return y("filter","blur(2px)");var e=i("a");return e.style.cssText=x.join("filter:blur(2px); "),!!e.style.length&&(n.documentMode===t||n.documentMode>9)}),s(),o(g),delete S.addTest,delete S.addAsyncTest;for(var k=0;k<Modernizr._q.length;k++)Modernizr._q[k]();e.Modernizr=Modernizr}(window,document);





