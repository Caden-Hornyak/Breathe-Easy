let friend_code_box = $('.friend-code');
let friend_code_box_focus = false;

let chat_message_input = $('.curr-chat-msg');
let chat_message_input_focus = false;

let body = $('body');
let message_list = $('.friend-list');
let user_chats_in;
let user_chats_store;

const chats = new Map();
let curr_chat_select;
let curr_chat_select_messages;

let friend_tab = $('.friend-tab');
let chat = $('.chat');


// Add Friend -- START
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
            // display whether friend is added or not
            
            let friend_req_msg = $('.friend_request_message');
            friend_req_msg[0].style.opacity = '1';
            if (data['added'] == 'true') {
                friend_req_msg[0].style.color = 'rgb(254, 255, 223);';
                friend_req_msg[0].innerHTML = "Friend request sent!";
            } else {
                friend_req_msg[0].style.color = 'rgb(227, 97, 97);';
                friend_req_msg[0].innerHTML = "User not found.";
            }

            setTimeout(function() {
                friend_req_msg[0].style.opacity = '0';
            }, 10000)
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}
// Add Friend -- END


// Get chats -- START
$('.create-chat').onclick = function() {
    $.ajax({
        type: 'POST',
        url: '/homepage/create_chat/',
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


// Get/Display user chats -- START
function get_user_chats(selected="") {
    $.ajax({
        type: 'POST',
        url: '/homepage/get_chats/',
        data: {
            'to_user': '',
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            user_chats_in = data['chats'];

            display_chats(selected);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}
get_user_chats();

function display_chats(selected="") {
    message_list.empty();

    if (user_chats_in.length > 0) {
        for (var i = 0; i < user_chats_in.length; i++) {

            var outer_div = document.createElement('div');
            outer_div.id = "friend-list-div-"+ i.toString();
            outer_div.className = 'friend-list-div';
        
            var chat_name = document.createElement('li');
            chat_name.className = 'chat-name';
            chat_name.textContent = user_chats_in[i][1];

            var chat_image = document.createElement('img');
            chat_image.className = 'chat-image';
            chat_image.src = "../../static/" + user_chats_in[i][2];
        
            var chat_date = document.createElement('li');
            chat_date.className = 'chat-date';
            chat_date.textContent = user_chats_in[i][3];
        
            outer_div.appendChild(chat_date);
            outer_div.appendChild(chat_image);
            outer_div.appendChild(chat_name);
            
            message_list[0].appendChild(outer_div);
            chats.set(outer_div.id, user_chats_in[i][0]);

            // switch between chats and friends tab
            outer_div.onclick = function() {
                $('.friends-tab-selector')[0].style.backgroundColor = 'transparent';
                if (curr_chat_select) {
                    curr_chat_select.style.backgroundColor = "transparent";
                }
                curr_chat_select = this;
                this.style.backgroundColor = "rgba(255, 255, 255, .2)";

                chat[0].style.opacity = '1';
                chat[0].style.pointerEvents = 'auto';
            
                friend_tab[0].style.opacity = '0';
                friend_tab[0].style.pointerEvents = 'none';

                get_message();
                
            }
            if (user_chats_in[i][0] == selected) {
                outer_div.click();
            }
        }
    } else {
        var no_friends = document.createElement('li');
        no_friends.textContent = "You have no chats";
        message_list[0].appendChild(no_friends);
    }
    
}
// Get/Display user chats -- END

// Get/Create/Destroy chat messages -- START
function create_destroy_message(action, text="") {

    $.ajax({
        type: 'POST',
        url: '/homepage/message_action/',
        data: {
            'action': action,
            'chat_id': chats.get(curr_chat_select.id),
            'text': text,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            get_message(curr_chat_select.id);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

function get_message() {

    $.ajax({
        type: 'POST',
        url: '/homepage/message_action/',
        data: {
            'action': 'get',
            'chat_id': chats.get(curr_chat_select.id),
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            curr_chat_select_messages = data['messages'];
            display_message(curr_chat_select_messages);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

function display_message(curr_chat_select_messages) {


    var ul = $('.message-list');
    ul.empty();

    // Append new messages to the ul
    curr_chat_select_messages.forEach(function(message_pair) {
        var div = document.createElement('div');
        if (message_pair[1]) {
            div.className = 'my-message';
        } else  {
            div.className = 'not-my-message'
        }
    
        var message = document.createElement('li');
        message.textContent = message_pair[0];

        div.appendChild(message);
            
        div.appendChild(message);
        ul[0].append(div);
    });

    // Scroll to the bottom of the ul
    ul.scrollTop(ul[0].scrollHeight);
}

chat_message_input[0].addEventListener("focus", (event) => {
    chat_message_input_focus = true;
  });

  chat_message_input[0].addEventListener("blur", (event) => {
    chat_message_input_focus = false;
  });

  friend_code_box[0].addEventListener("focus", (event) => {
    friend_code_box_focus = true;
  });

  friend_code_box[0].addEventListener("blur", (event) => {
    friend_code_box_focus = false;
  });

body[0].addEventListener('keydown', function(event) {

    if (event.key === 'Enter') {

        if (friend_code_box_focus) {
            send_friend_code();
        }

        if (chat_message_input_focus) {
            let message = chat_message_input[0].value;
            chat_message_input[0].value = "";
            create_destroy_message('create', message);
        }

    }
});

// switch from chat tab to friends tab
$('.friends-tab-selector')[0].onclick = function() {

    if (curr_chat_select) {
        curr_chat_select.style.backgroundColor = "transparent";
    }
    $('.friends-tab-selector')[0].style.backgroundColor = "rgba(255, 255, 255, .2)";
    chat[0].style.opacity = '0';
    chat[0].style.pointerEvents = 'none';

    friend_tab[0].style.opacity = '1';
    friend_tab[0].style.pointerEvents = 'auto';
    get_friendtab_friends();

}

// Friend Tab -- START
let friends_tab_friends;
let friend_tab_list = $('#friend-tab-list');

function get_friendtab_friends() {
    $.ajax({
        type: 'POST',
        url: '/homepage/friends/',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            friends_tab_friends = data['friends'];
            display_friendtab_friends();
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}


function display_friendtab_friends() {
    friend_tab_list.empty();
    for (var i = 0; i < friends_tab_friends.length; i++) {
        var div = document.createElement('div');
        div.className = 'friend-tab-div';

        var img = document.createElement('img');
        img.className = 'friend-tab-img';
        img.src = friends_tab_friends[i][1];

        var li = document.createElement('li');
        li.className = 'friend-tab-span';
        li.innerHTML = friends_tab_friends[i][0];

        var span = document.createElement('span');
        span.style.color = "rgba(254, 255, 223, .2)";

        var circle = document.createElement('div');
        circle.className = 'circle';

        // if friend is active
        if (friends_tab_friends[i][2]) {

            circle.style.background = "rgb(254, 255, 223)";
            span.innerHTML = 'Active';
        } else {

            circle.style.background = "rgba(254, 255, 223, .4)";
            span.innerHTML = 'Offline';
        }

        div.appendChild(img);
        div.appendChild(li);
        div.append(span);
        div.appendChild(circle);
        friend_tab_list[0].append(div);
    }
}

$('.friends-tab-selector').click();

$("#friends-tab-btn2")[0].onclick = function() {

    $("#friend-tab-friendreq")[0].style.display = 'block';
    $("#friend-tab-friends")[0].style.display = 'none';
}

$("#friends-tab-btn")[0].onclick = function() {
    
    $("#friend-tab-friendreq")[0].style.display = 'none';
    $("#friend-tab-friends")[0].style.display = 'block';
}

$("#friends-tab-btn").click();


let friends_tab_friendreq;
let friends_tab_friendreq_list = $('#friend-tab-list2');

function get_friendtab_friendreq() {
    $.ajax({
        type: 'POST',
        url: '/homepage/get_friend_request/',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            friends_tab_friendreq = data['friend_requests'];
            display_friendtab_friendreq();
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

//friend request tab
function display_friendtab_friendreq() {
    friends_tab_friendreq_list.empty();

    if (friends_tab_friendreq.length  == 0) {
        var span = document.createElement('span');
        span.innerHTML = "You have no friend requests";
        friends_tab_friendreq_list[0].append(span);
    } else {
        for (var i = 0; i < friends_tab_friendreq.length; i++) {

            var div = document.createElement('div');
            div.className = 'friend-tab-div';
    
            var img = document.createElement('img');
            img.className = 'friend-tab-img';
            img.src = friends_tab_friendreq[i][1];

    
            var li = document.createElement('li');
            li.className = 'friend-tab-span';
            li.innerHTML = friends_tab_friendreq[i][0];
    
            var check = document.createElement('i');
            check.classList.add("bx", "bx-check");
    
            var x = document.createElement('i');
            check.className = "block";
    
    
            div.appendChild(img);
            div.appendChild(li);
            div.appendChild(check);
            div.appendChild(x);
    
            friends_tab_friendreq_list[0].append(div);
        }
    }
    
}

get_friendtab_friendreq();