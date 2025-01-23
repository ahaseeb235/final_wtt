
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






// Hours Worked Chart
// document.addEventListener('DOMContentLoaded', function () {
//     const ctx = document.getElementById('chart-container').getContext('2d');
//     const chart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: [{% for workday in workdays %}"{{ workday.user.get_full_name }}",{% endfor %}],
//             datasets: [{
//                 label: 'Total Hours Worked',
//                 data: [{% for workday in workdays %}{{ workday.total_hours|floatformat:2 }},{% endfor %}],
//                 backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// });

// Message/Notification timer

// var message_timeout = document.getElementById("message-timer");

// setTimeout(function () {

//     message_timeout.style.display = "none";


// }, 3000);
