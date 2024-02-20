let left = $('.left');
let right = $('.right');
let lr_active = false;
let clone;
let reg_title1 = $("#reg-title"), log_title1 = $("#login-title");


// On page load, display "register" and "login"
document.addEventListener('DOMContentLoaded', function() {
    
    reg_title1[0].style.opacity = "1";
    log_title1[0].style.opacity = "1";
}, false);

// change titles based off states of left and right
function lr_change(l_toggle, r_toggle) {
    left[0].classList.toggle(l_toggle);
    right[0].classList.toggle(r_toggle);

    if (!lr_active) {
        visib = 'hidden';
    } else {
        visib = 'visible';
    }
    reg_title1[0].style.visibility = visib;
    log_title1[0].style.visibility = visib;
}

// left click = load register
left[0].onclick = function() {
    let regwrapper = $(".reg-wrapper");

    // scroll background, hide titles
    lr_change('active', 'deactive');

    // on left click, display register page or remove it if already active
    if (!lr_active) {
        lr_active = true;

        clone = regwrapper.clone();

        // get register.html, set register to visible
        $.get("register", function(data) { $("#reg-placeholder").replaceWith(data); });
        regwrapper[0].classList.toggle('active');
        

        moniterTagSelect();
        
        
    } else {
        lr_active = false;

        regwrapper.replaceWith(clone);
        regwrapper[0].classList.toggle('active');
    }
    
};


// right click = load login
right[0].onclick = function() {
    let loginwrapper = $(".login-wrapper");
    
    // scroll background
    lr_change('deactive', 'active');
    
    // on right click, display login page or remove it if already active
    if (!lr_active) {
        lr_active = true;

        clone = loginwrapper.clone()

        // get login.html, set login to visible
        $.get("login", function(data) { $("#log-placeholder").replaceWith(data); });
        loginwrapper[0].classList.toggle('active');

        
    } else {
        lr_active = false;

        loginwrapper.replaceWith(clone);
        loginwrapper[0].classList.toggle('active');
    }

    
};

// error message handling
if (side == 'right') {
    right.click();
} else if (side == 'left') {
    left.click()
}


function checkSubmit(e) {
    if (e.key == 'Enter') {
        return false;
    } else {

        // Access the form element
        $('.regform').append('<input type="hidden" id="yourData" name="tags" value="'+ tags +'"/>');

        return true;
    }
    
}








