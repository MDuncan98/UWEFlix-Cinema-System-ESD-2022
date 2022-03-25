$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });

    function updateTickets(p1, value, cValue) {
        cValue = cValue + p1 * value;
        $("#id_total_cost").val('');
        $("#id_total_cost").val(cValue);
        alert(cValue);
        //Find way to get ticket price information from file
        //Calculate cost
        //Display in text field
    }

    $("#id_adult_tickets").change(function() {
        var str = $("#id_adult_tickets").val();
        var currVal = $("#id_total_cost").val();
        updateTickets(str, 5, currVal);
    });

    $("#id_student_tickets").change(function() {
        alert("Hello!")
    })

    $("#id_child_tickets").change(function() {
        alert("Hello!")
    })
});