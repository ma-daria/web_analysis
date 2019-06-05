disabledSelect();


function disabledButton(){
    but = document.getElementById("but");
    but.disabled = true;
}

function undisabledButton(){
    but = document.getElementById("but");
    but.disabled = false;
}


function disabledSelect(){
    but = document.getElementById("name2");
    but.disabled = true;
}

function undisabledSelect(){
    but = document.getElementById("name2");
    but.disabled = false;
}

$("#name2").change(function(){
    var minimum = 2;
    len = $(".js-example-basic-multiple").select2('data').length;
     if(len>=minimum){
         undisabledButton();
     }else {
         disabledButton();
     }
});

$("#name3").change(function(){
    text = document.getElementById("name3");
    if (text.value === 'Корреляция химического и видового состава') {
        undisabledSelect();
        disabledButton();
    }else {
        disabledSelect();
    }

});


$(document).ready(function() {
    $("#name").select2();
});



