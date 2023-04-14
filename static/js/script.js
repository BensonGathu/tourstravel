$(document).ready(function() {
    $("#book").click(function(e) {
        e.preventDefault();
        $("#payment-button-amount").hide();
        $("#payment-button-amount").show();
    });

});


function calcPrice(){
    var noMembers= document.getElementsByClassName("memb")[0].value;
    console.log(noMembers);
    var tripAmount= document.getElementsByClassName("tripAmount")[0].value;
    if (noMembers) {
        var totalPrice = tripAmount * noMembers;
        console.log(totalPrice);
        console.log(document.getElementsByClassName("totalPrice"))
        document.getElementsByClassName("totalPrice")[0].innerHTML= `Total KSH ${totalPrice}`
        document.getElementsByClassName("totalPriceView")[0].value=totalPrice
    }
    else{
        document.getElementsByClassName("totalPrice")[0].innerHTML= `Total KSH ${tripAmount}`

    }
   

}
