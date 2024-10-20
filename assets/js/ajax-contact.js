(function ($) {
    'use strict';

    var form = $('.contact_form'),
        message = $('.contact_msg'),
        form_data;

    // Success function
    function done_func(response) {
        if (response.status === 1) {
            message.fadeIn().removeClass('alert-danger').addClass('alert-success');
            message.text(response.msg);

            setTimeout(function () {
                message.fadeOut();
            }, 3000);
            form.find('input:not([type="submit"]), textarea').val('');
            if ($.trim(response.url)) {
                window.location.href = response.url
            }

        } else if (response.status === 2) {
            message.fadeIn().removeClass('alert-success').addClass('alert-danger');
            message.text(response.msg);

            setTimeout(function () {
                message.fadeOut();
            }, 3000);
            form.find('input:not([type="submit"]), textarea').val('');
        } else if (response.status === 3) {
            message.fadeIn().removeClass('alert-success').addClass('alert-danger');
            message.text(response.msg);
            setTimeout(function () {
                message.fadeOut();
            }, 3000);
            form.find('input:not([type="submit"]), textarea').val('');
        }
    }

    // fail function
    function fail_func(data) {
        message.fadeIn().removeClass('alert-success').addClass('alert-success');

        message.text(data);
        setTimeout(function () {
            message.fadeOut();
        }, 2000);
    }

    form.submit(function (e) {
        e.preventDefault();
        form_data = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form_data,
            cache: false,
            async: true
        })
            .done(done_func)
            .fail(fail_func);
    });

})(jQuery);




















