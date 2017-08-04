$(function(){
    "use strict";

    $(document).on("ready",function () {
        $("select[name=examine]").each(function() {
            $(this).val( function() {
                return $(this).find("option[selected]").attr("value");
            })
        });
    })

    // 将路径里的变量转换成对象
    function urlToObj(str){
        var url = str || window.location.search.substring(1);
        var urlArray = url.split("&");
        var obj =  new Object();
        var arr = [];
        var len = urlArray.length;
        var sort = $(".sort");
        for(var i = 0; i <  len; i++){
            if(urlArray[i].indexOf("=") >= 0){
                arr = urlArray[i].split("=");
                obj[arr[0]] = arr[1];
            }
        }
        sort.removeClass("desc");
        sort.removeClass("asc");

        if (obj.sort == 1) {
            sort.removeClass("asc");
            sort.addClass("desc");
        } else if (obj.sort == -1) {
            sort.removeClass("desc");
            sort.addClass("asc");
        }

        return obj;

    }
    init();
    function init(){
        var url = $(".order-by").attr("href");
        var key = $(".order-by").data("key");
        var obj = urlToObj();
        var value = obj[key] || 1;
        value = parseInt(value);
        value = - value;
        url = url + "?" + key + "=" + value;
        $(".order-by").attr("href", url);
    }

    //改状态
    $("body").on("change",".status select",function(){
        var val = $(this).val(),
            url = $(this).attr("data-url"),
            text =  $(this).find("option:selected").text(),
            obj = $(this).parents(".status").find("em");

        $.get(url,{'examine':val}, function (res) {
            if(res.state){
                obj.html(text);
            }
        })
    })

    //关注取消关注
    $("body").on("click", ".attention span", function () {
        var url = $(this).find("a").attr("data-url"),
            attention = $(this).find("a").attr("data-attention");
        var obj = $(this).parents(".attention");
        $.get(url,{'attention':attention},function(res){
            if(res.state){
                if(res.data.attention == 0){
                    var yesHtml = "<span class='yes'>" +
                                    "<em class='yes-img'></em>" +
                                    "<a href='javascript:void (0)' data-url='"+
                                    url+
                                    "' data-attention='"+res.data.attention+
                                    "'>"+res.data.attention_display+
                                    "</a>" +
                                    "</span>";
                    obj.find("span").remove();
                    obj.append(yesHtml);
                }else{
                    var noHtml =  "<span class='no'>" +
                                    "<a href='javascript:void (0)' data-url='"+
                                    url+
                                    "' data-attention='"+res.data.attention+
                                    "'>"+res.data.attention_display+
                                    "</a>" +
                                    "</span>";
                    obj.find("span").remove();
                    obj.append(noHtml);
                }
            }
        })
    })
});