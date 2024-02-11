let left = document.querySelector('.left');
let right = document.querySelector('.right');
let authDisp = false;
let clone;

left.onclick = function () {
    left.classList.toggle('active');
    right.classList.toggle('deactive');
    if (!authDisp) {
        clone = $("#loadreg").clone(true, true);
        $.get("signup", function(data){
        $("#register").replaceWith(data);
        });
        authDisp = true;
    } else {
        $("#loadreg").replaceWith(clone);
        authDisp = false;
    }
    
};

right.onclick = function () {
    left.classList.toggle('deactive');
    right.classList.toggle('active');
    
    if (!authDisp) {
        clone = $("#loadlog").clone(true, true);
        $.get("signin", function(data){
            console.log("hello");
            $("#signin").replaceWith(data);
        });
        authDisp = true;
    } else {
        $("#loadlog").replaceWith(clone);
        authDisp = false;
    }
};

function clearcontent(elementID) { 
    document.querySelector('.left').innerHTML = ""; 
} 


