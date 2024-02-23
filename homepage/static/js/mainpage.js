let inside_btn = $("#inside-btn");
let outside_btn = $("#outside-btn");
let output = $("#output");
let output_wrapper = $(".output-wrapper");
let chatbot_output;
let blinking_rectangle = $(".blinking-rectangle");
let mainpage = $(".mainpage");



// On page load, display all button elements
document.addEventListener('DOMContentLoaded', function() {
    show_titles(isNewUser);
    
}, false);

function show_titles(new_user) {
    if (new_user) {
        setTimeout(function () {
            $('.fade-in').each(function() {
                $(this)[0].style.opacity = "1";
                $(this)[0].style.pointerEvents = "auto";
             });
        }, 12000);
    } else {
        $('.fade-in').each(function() {
            $(this)[0].style.opacity = "1";
            $(this)[0].style.pointerEvents = "auto";
         });
    }
    
}

function hide_titles() {
    inside_btn[0].style.opacity = "0";
    outside_btn[0].style.opacity = "0";
    inside_btn[0].style.pointerEvents = "none";
    outside_btn[0].style.pointerEvents = "none";
}

function display_output(index) {
    output[0].textContent += chatbot_output[index] + " ";

    if (index < chatbot_output.length) {
        setTimeout(function() {
            display_output(index+1);
        }, 60);
    } else {
        blinking_rectangle[0].classList.toggle("paused");
    }
}


window.send_user_data = function send_user_data(button) {
    console.log("chatbot_called :)")
    hide_titles();

    var userInput = button.innerText;

    //while testing
    // let text = "I'm glad to hear that you enjoy rap and hip-hop music! Here are some popular rap and hip-hop songs without any explanations:"
    // chatbot_output = text.split(" ")       
    // output_wrapper[0].style.opacity = "1";   
    // blinking_rectangle[0].classList.toggle("paused");
    // display_output(0);
    // return;

    $.ajax({
        type: 'POST',
        url: '/homepage/prompt_reciever/',
        data: {
            'user_input': userInput,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {

            // prompt form string to list
            chatbot_output = data.chatbot_response.split(" ")
            
            output_wrapper[0].style.opacity = "1";   
            blinking_rectangle[0].classList.toggle("paused");
            display_output(0);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
   
}

// window.friends_tab = function friends_tab() {
//     mainpage[0].classList.toggle("active");
// }

let homepage_wrapper = $('.homepage-wrapper');
let friend_wrapper = $('.friend-wrapper');

$('#friends-btn')[0].onclick = function() {
    friend_wrapper[0].style.left = '0vw';
    homepage_wrapper[0].style.right = '100vw';
}

$('#homepage-btn')[0].onclick = function() {
    friend_wrapper[0].style.left = '100vw';
    homepage_wrapper[0].style.right = '0vw';
}