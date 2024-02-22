let friend_selector = $('.friend-selector');
let create_chat_btn = $('.create-chat');
let friend_list = $('.selector-friend-list');

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

console.log(friend_selector[0]);
friend_selector[0].onclick = function(event) {
    event.stopPropagation(); 
}

document.addEventListener('click', function() {
    friend_list.empty()
    friend_selector[0].style.opacity = '0';
    friend_selector[0].style.pointerEvents = 'none';
});


function get_friends() {
    let friends;
    $.ajax({
        type: 'POST',
        url: '/homepage/friends/',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (data) {
            friends = data['friends']
            display_friends(friends)
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });


}

function display_friends(friends) {
    if (friends.length > 0) {
        for (var i = 0; i < friends.length; i++) {
            var checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = 'checkbox-' + i.toString();

            var label = document.createElement('label');
            label.for = 'checkbox-' + i.toString();
            label.innerHTML = friends[i][0];

            var prof_pic = document.createElement('img');
            prof_pic.src = friends[i][1];

            var div = document.createElement('div');
            div.className = 'selector-friend-li';
            div.appendChild(prof_pic);
            div.appendChild(label);
            div.appendChild(checkbox);
            
            friend_list[0].append(div);
        }
    } else {
        // you have no friends
    }
}

$('.friend-selector-submit').onclick = function() {

}

$('.friend-tag-selector').keypress(function() {
    this.rows = Math.floor(this.value.length / 25) + 1;
})