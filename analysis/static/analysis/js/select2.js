disabled();
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
     if($(".js-example-basic-multiple").select2('data').length>=minimum){
         undisabled();
     }
     else {
         disabled()
     }
});


$(document).ready(function() {
    $("#name").select2();
});



