$('.loader').show();
$('.container').hide();

function show_loader(){
    $('.container').hide();
    $('.loader').show();
}
function hide_loader(){
    $('.loader').hide();
    $('.container').show();
}

$('#but').click(function () {
    show_loader();
});

$('.nav-item').click(function () {
    console.log('wow');
    show_loader();
});

$(window).on('load', function () {
    hide_loader();
});
