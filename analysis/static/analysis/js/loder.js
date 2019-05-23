$('.loader').hide();

function fun(){
    $('.container').hide();
    $('.loader').show();
}

$('#but').click(function () {
    fun();
});

$('.dropdown-item').click(function () {
    fun();
});