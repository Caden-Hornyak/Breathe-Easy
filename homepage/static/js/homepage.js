
// On page load, display "register" and "login"
// document.addEventListener('DOMContentLoaded', function() {
//     show_titles(isNewUser);

// }, false);

// function show_titles(new_user) {
//     if (new_user) {
//         setTimeout(function () {
//             document.getElementById('instructionsList').style.display = 'none';
//             // Add code here to display something else after 12 seconds
//         }, 12000);
//     } else {

//     }
// }

window.send_user_data = function send_user_data(button) {
    var userInput = button.innerText;
    let chatbot_output;

    $.ajax({
        type: 'POST',
        url: '/homepage/ajax/',
        data: {
            'user_input': userInput,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            chatbot_output = data.chatbot_response;
            console.log(chatbot_output);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
   
}