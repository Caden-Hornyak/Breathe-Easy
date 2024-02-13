let left = document.querySelector('.left');
let right = document.querySelector('.right');
let authDisp = false;
let clone;

left.onclick = function () {
    let loadreg = document.querySelector(".loadreg");
    left.classList.toggle('active');
    right.classList.toggle('deactive');
    if (!authDisp) {
        clone = $("#loadreg").clone(true, true);
        loadreg.classList.toggle('active');
        $.get("signup", function(data){
        $("#register").replaceWith(data);
        });

        moniterTagSelect();
        authDisp = true;
        
    } else {
        $("#loadreg").replaceWith(clone);
        loadreg.classList.toggle('active');
        authDisp = false;
        tsInput = false;
    }
    
};

right.onclick = function () {
    let loadlog = document.querySelector(".loadlog");
    left.classList.toggle('deactive');
    right.classList.toggle('active');
    
    if (!authDisp) {
        clone = $("#loadlog").clone(true, true);
        $.get("signin", function(data){
            $("#signin").replaceWith(data);
        });
        loadlog.classList.toggle('active');
        authDisp = true;
    } else {
        loadlog.classList.toggle('active');
        $("#loadlog").replaceWith(clone);
        authDisp = false;
    }
};

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("reg").style.opacity = "1";
    document.getElementById("li").style.opacity = "1";
}, false);

function checkSubmit(e) {
    if (e.key == 'Enter') {
        return false;
    } else {

        // Access the form element
        $('form-div').append('<input type="hidden" id="yourData" name="tags" value="'+ tags +'"/>');

        setTimeout(function() {
        // Submit the form
        form.submit();
        }, 100000);
    }
}








