
// Initialize Flatpickr
flatpickr("input[name='date']", {
    altInput: true,
    altFormat: "F j, Y",
    dateFormat: "Y-m-d",
});

flatpickr("input[name='time_in']", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    enableTime: true,
});

flatpickr("input[name='time_out']", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    enableTime: true,
});




// Message/Notification timer

// var message_timeout = document.getElementById("message-timer");

// setTimeout(function () {

//     message_timeout.style.display = "none";


// }, 3000);
