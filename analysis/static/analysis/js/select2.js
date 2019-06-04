// disabled();
function disabled(){
    but = document.getElementById("but");
    but.disabled = true;
}

function undisabled(){
    but = document.getElementById("but");
    but.disabled = false;
}


$("#name2").change(function(){
    var minimum = 2;
    len = $(".js-example-basic-multiple").select2('data').length
     if(len>=minimum || len === 0){
         undisabled();
     }
     else {
         disabled()
     }
});


$(document).ready(function() {
    $("#name").select2();
});



