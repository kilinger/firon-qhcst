$(function(){
    var templates = Handlebars.templates = Handlebars.templates || {};
        templates.demand = Handlebars.compile($("#demand-created-template").html());

    $("body").on("click",".demand_create",function(){
         $(templates.demand()).appendTo(".form-horizontal");
         $(this).remove();
    });
    if(!Modernizr.inputtypes.date){
        $(".date").attr("readonly","readonly");
        $(".date").datetimepicker({
            format: 'yyyy-mm-dd',
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 2,
            minView: 2
        });
    }
})