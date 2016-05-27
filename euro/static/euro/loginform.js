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
            location.reload();
        }
    }
    , error: function (jqXHR, textStatus, errorThrown) {
        alert('error: ' + textStatus + errorThrown);
    }
};

$(function () {
    form.init($('#login')); // initialize form
});


$(document).ready(function () {

    $('.form-control').keypress(function () {
        $('.log-status').removeClass('wrong-entry');
        $('.log-btn').removeClass('wrong-entry');
        document.getElementById('log-btn').textContent = 'Log in';
    });

});