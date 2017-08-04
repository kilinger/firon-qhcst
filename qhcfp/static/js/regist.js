$(function(){
    "use strict";

    $("body").on("change",".radio-box",function(){
        $(this).siblings(".active").removeClass("active");
        $(this).addClass("active");
    })
    $("body").on("click",".slider",function(){
        $(this).toggleClass("close");
    })
    $("body").on("click",".information",function (){
        var url = $(".form-horizontal").attr("action");
        var formData = $(".form-horizontal").serializeArray();
        $.post(url,formData,function(res){
            if(res.state){
                window.location.href = res.url;
            }
        }, "json");
    })
})