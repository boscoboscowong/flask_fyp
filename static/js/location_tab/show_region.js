function show_HKI(){
    $(".HKI").each(function(){
       $(this).show();
    });

    $(".KLN, .NT").each(function(){
        $(this).hide();
    });

    $("#HKI").addClass("active");
    $("#KLN").removeClass("active");
    $("#NT").removeClass("active");
}

function show_KLN(){
    $(".KLN").each(function(){
       $(this).show();
    });

    $(".HKI, .NT").each(function(){
        $(this).hide();
    });

    $("#KLN").addClass("active");
    $("#HKI").removeClass("active");
    $("#NT").removeClass("active");
}

function show_NT(){
    $(".NT").each(function(){
       $(this).show();
    });

    $(".KLN, .HKI").each(function(){
        $(this).hide();
    });

    $("#NT").addClass("active");
    $("#KLN").removeClass("active");
    $("#HKI").removeClass("active");
}
