disabledSelect();
check_name3();
tab();

function disabledButton(){
    but = document.getElementById("but");
    but.disabled = true;
}

function undisabledButton(){
    but = document.getElementById("but");
    but.disabled = false;
}

function hidePairplot() {
    $(".additional").hide();
}

$('img').on( "error", function() {
    hidePairplot()
});


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
    check_name3();
});

function check_name3() {
    text = document.getElementById("name3");
    if (text.value === 'Задать вручную') {
        undisabledSelect();
        disabledButton();
    }else {
        disabledSelect();
        undisabledButton();
    }
}

function tab() {
    var table=document.getElementById('corMax');
    console.log(table.rows.length);
    if (table.rows.length === 1){

        $('#corMax tbody').prepend("<tr><td>Таких значений нет</td></tr>")
    }
}