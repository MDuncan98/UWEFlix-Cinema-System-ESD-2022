$(document).ready( function() {
    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });

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
                //cValue = at * value;
        $("#id_total_cost").val('');
        $("#id_total_cost").val(totalPrice);
        //alert(totalPrice);
        //Find way to get ticket price information from file
        //Calculate cost
        //Display in text field
    }

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
});