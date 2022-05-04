$(document).ready( function() {
    var discountApplied = false;

    function applyDiscount(cValue, discRate){
        if (cValue != 0.00) {
            discountedValue = cValue * discRate;
            discountedValue = parseFloat(discountedValue).toFixed(2);
            $("#id_total_cost").val(discountedValue);
            discountApplied = true;
            $("#discount-btn").prop('disabled', true);
        }
    }
    
    function updateTickets(at, st, ct) {
        adultPriceHTML = document.getElementById("payment_adult_price").innerHTML;
        adultPrice = parseFloat(adultPriceHTML);
        studentPriceHTML = document.getElementById("payment_student_price").innerHTML;
        studentPrice = parseFloat(studentPriceHTML);
        childPriceHTML = document.getElementById("payment_child_price").innerHTML;
        childPrice = parseFloat(childPriceHTML);
        totalPrice = 0;
        
        if (at != '') {
            cValue = at * adultPrice;
            totalPrice = totalPrice + cValue;
        }
        if (st != '') {
            cValue = st * studentPrice;
            totalPrice = totalPrice + cValue;
        }
        if (ct != '') {
            cValue = ct * childPrice;
            totalPrice = totalPrice + cValue;
        }
        if (discountApplied == true) {
            applyDiscount(totalPrice, 0.9);
        }
        else {
            display = parseFloat(totalPrice).toFixed(2)
            $("#id_total_cost").val(display);
        }
    }

    function updateTicketsRep(amt) {
        studentPriceHTML = document.getElementById("rep_payment_student_price").innerHTML;
        studentPrice = parseFloat(studentPriceHTML);
        //studentPrice = 4;  
        totalPrice = 0 
        if (amt != '') {
            totalPrice = totalPrice + (amt * studentPrice);
        }
        discount_rate_html = document.getElementById("discount_rate").innerHTML;
        discount_rate_float = parseFloat(discount_rate_html);
        if (!isNaN(discount_rate_float)) {
            discountRate = discount_rate_float;
            totalPrice = totalPrice * discountRate;
        }
        display = parseFloat(totalPrice).toFixed(2)
        $("#id_total_cost").val(display);
    }

    $("#discount-btn").click( function(event) {
        if ($("#id_total_cost").val() != 0.00) {
            $("#cancel-discount-btn").show();
            applyDiscount($("#id_total_cost").val(), 0.9);
        }
    });

    $("#cancel-discount-btn").click(function(event) {
        discountApplied = false;
        $("#discount-btn").prop('disabled', false);
        $("#cancel-discount-btn").hide();
        updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
    })


    $("#id_adult_tickets").change(function() {
        if ($("#id_adult_tickets").val() < 0) {
            $("#id_adult_tickets").val(0);
        }
        else {
            updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
        }
    });

    $("#id_student_tickets").change(function() {
        if ($("#id_student_tickets").val() < 0) {
            $("#id_student_tickets").val(0);
        }
        else {
            updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
        }    })

    $("#id_child_tickets").change(function() {
        if ($("#id_child_tickets").val() < 0) {
            $("#id_child_tickets").val(0);
        }
        else {
            updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
        }    })

    $("#id_rep_student_tickets").change(function() {
        if ($("#id_rep_student_tickets").val() < 10) {
            $("#id_rep_student_tickets").val(10);
        }
        updateTicketsRep($("#id_rep_student_tickets").val())    
    })

    $("#payment-form").submit(function() {
        $("#id_total_cost").prop('disabled', false);
    });
});