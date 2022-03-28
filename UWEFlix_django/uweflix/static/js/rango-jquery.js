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
        adultPrice = 5;
        studentPrice = 4;
        childPrice = 3;
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
            //alert(totalPrice);
        }
        //alert(totalPrice);
        //Find way to get ticket price information from file
        //Calculate cost
        //Display in text field
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
            //alert("no");
            $("#id_adult_tickets").val(0);
        }
        else {
            updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
        }
    });

    $("#id_student_tickets").change(function() {
        if ($("#id_student_tickets").val() < 0) {
            //alert("no");
            $("#id_student_tickets").val(0);
        }
        else {
            updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
        }    })

    $("#id_child_tickets").change(function() {
        if ($("#id_child_tickets").val() < 0) {
            //alert("no");
            $("#id_child_tickets").val(0);
        }
        else {
            updateTickets($("#id_adult_tickets").val(), $("#id_student_tickets").val(), $("#id_child_tickets").val());
        }    })

    $("#payment-form").submit(function() {
        $("#id_total_cost").prop('disabled', false);
    });
});