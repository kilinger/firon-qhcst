$(function(){
    "use strict";

    function updateQueryStringParameter(uri, key, value) {
        var re = new RegExp("([?|&])" + key + "=.*?(&|$)", "i"),
          separator = uri.indexOf('?') !== -1 ? "&" : "?";
        if (uri.match(re)) {
            return uri.replace(re, '$1' + key + "=" + value + '$2');
        } else {
            return uri + separator + key + "=" + value;
        }
    }

    //导出表格
    $(".export-table").click(function() {
        $(this).attr("href", updateQueryStringParameter(window.location.href, 'export', '1')).attr("target", "_blank");
    });


    //导入表格弹窗
    var templates = Handlebars.templates = Handlebars.templates || {};
        templates.import = Handlebars.compile($("#import-table-template").html());

    $("body").on("click", ".import-table", function(e){
        e.preventDefault();
        $(templates.import()).appendTo("body").bPopup({
            modalClose: false,
            opacity: 0.3,
            modalColor: 'black',
            followSpeed: 200,
            onClose: function() {
                $(this).remove();
            }
        })
    })

    $("body").on("click",".sub",function(e){
        e.preventDefault();
        $("#table-form-horizontal").ajaxSubmit({
            dataType: "json",
            beforeSubmit:function(){
                $("#upload-status").html("");
            },
            success:function(response){
                if(response.state){
                    window.top.location.href = response.reverse_url;
                }else if(response.error){
                    $("#upload-status").html(response.error.upload_xls[0]);
                }else{
                    $("#upload-status").html(response.data);
                }
            }
        });

        return;
    });

})