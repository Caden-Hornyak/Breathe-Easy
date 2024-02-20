let friend_code_box = $('.friend-code');
let body = $('body');
let friend_code_box_focus = false;

// Add Friend -- START
friend_code_box[0].addEventListener("focus", (event) => {
    event.target.style.background = "pink";
    friend_code_box_focus = true;
  });

  friend_code_box[0].addEventListener("blur", (event) => {
    event.target.style.background = "white";
    friend_code_box_focus = false;
  });

body[0].addEventListener('keydown', function(event) {

    if (event.key === 'Enter') {
        if (friend_code_box_focus) {
            send_friend_code();
            friend_code_box[0].value = "";
        }

    }
});

function send_friend_code() {
    let friend_username = friend_code_box[0].value;
    friend_code_box[0].value = "";

    $.ajax({
        type: 'POST',
        url: '/homepage/send_friend_request/',
        data: {
            'to_user': friend_username,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            console.log(data['response']);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}
// Add Friend -- END

// Friend Sidebar -- START

$('.friend-list-div').each(function(){
    $(this)[0].onclick = function() {
        $.ajax({
            type: 'GET',
            url: '/homepage/send_friend_request/',
            data: {
                'to_user': friend_username,
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data['response']);
            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    }
 });

// $('.chat')[0].onclick = function() {
//     $.ajax({
//         type: 'GET',
//         url: '/homepage/message_action/',
//         data: {
//             'action': 'create',
//             'chat_id': '-',
//             'participants': 'participants',
//             'text': 'text',
//             'message_owner':'message_owner',
//             csrfmiddlewaretoken: window.CSRF_TOKEN,
//         },
//         dataType: 'json',
//         success: function (data) {
//             console.log(data['response']);
//         },
//         error: function (error) {
//             console.error('Error:', error);
//         },
//     });
// }
