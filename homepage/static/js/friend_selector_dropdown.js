let friend_selector = $('.friend-selector');
let create_chat_btn = $('.create-chat');
let friend_list = $('.selector-friend-list');
let friends;
let checkbox_dic = {};


create_chat_btn[0].onclick = function(event) {
    
    if (friend_selector[0].style.opacity != '1') {
        event.stopPropagation(); 
    } else {
        return;
    }

    friend_selector[0].style.opacity = '1';
    friend_selector[0].style.pointerEvents = 'auto';
    get_friends();
}

friend_selector[0].onclick = function(event) {
    event.stopPropagation(); 
}

document.addEventListener('click', function() {
    friend_list.empty()
    friend_selector[0].style.opacity = '0';
    friend_selector[0].style.pointerEvents = 'none';
});


function get_friends() {
    
    $.ajax({
        type: 'POST',
        url: '/homepage/friends/',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            friends = data['friends'];
            display_friends()
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });


}

// displays friends on the create chat selector
function display_friends(match="") {
    friend_list.empty();

    if (friends.length > 0) {
        for (var i = 0; i < friends.length; i++) {
            if (match == "" || (friends[i][0].toLowerCase()).search((match.toLowerCase())) != -1) {
                var checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = 'checkbox-' + i.toString();
                checkbox.className =  friends[i][0]
                if (friends[i][0] in checkbox_dic && checkbox_dic[friends[i][0]]) {
                    checkbox.checked = true;
                }

                var label = document.createElement('label');
                label.for = 'checkbox-' + i.toString();
                label.innerHTML = friends[i][0];

                var prof_pic = document.createElement('img');
                prof_pic.src = friends[i][1];

                var div = document.createElement('div');
                div.className = 'selector-friend-li';
                
                // remember checkbox states
                (function(checkbox) {
                    div.onclick = function() {
                        checkbox.checked = !checkbox.checked;
                        checkbox_dic[checkbox.className] = checkbox.checked;
                    }
                })(checkbox);

                div.appendChild(prof_pic);
                div.appendChild(label);
                div.appendChild(checkbox);
                
                friend_list[0].append(div);
            }
        }
    } else {
        // you have no friends
    }
}

// submit form
$('.friend-selector-submit')[0].onclick = function(e) {
    console.log("ran");
    let selected_friends = [];
    for (var element in checkbox_dic) {
        if (checkbox_dic[element]) {
            selected_friends.push(element);
        }   
    }
    $.ajax({
        type: 'POST',
        url: '/homepage/create_chat/',
        data: {
            'friends': JSON.stringify(selected_friends),
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            chat = data['chat'];
            get_user_chats(chat);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

// handles textarea expansion with text
let friend_area = $('.friend-tag-selector')[0];
friend_area.addEventListener("keyup", e=> {
    friend_selector[0].style.height = "200px";
    friend_area.style.height = "25px";
    let scHeight = e.target.scrollHeight;
    friend_area.style.height = `${scHeight}px`;
    friend_selector[0].style.height = (200 - 25 + scHeight).toString() + 'px';
    display_friends(friend_area.value);
});