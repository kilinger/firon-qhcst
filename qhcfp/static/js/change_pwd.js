$(function(){
    $("body").on("submit",function(e) {
        e.preventDefault();
        if ($(this).hasClass("posting")) {
            return false;
        }
        $(this).addClass("posting");

        var formData = $(".form-horizontal").serializeArray(),
            url = $(".form-horizontal").attr("action");

        $.post(url, formData, function (resp) {
            if (resp.state) {
                window.location = resp.redirect_url;
            }else {
                var i = 0;
                for(var name in resp.error) {
                    i++;
                    $("#div_id_"+name).find(".error-msg").remove().end().parents(".control")
                        .append('<div class="error-msg">'+ resp.error[name] +'</div>');
                    if(i == 1) {
                        $("#id_" + name).focus();
                    }
                }
                i = null;
            }
        })
    })
})