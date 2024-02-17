let maxTags = 7;
let tags = [];
let tagNumb;
let input;
let ul;


function moniterTagSelect() {
    setTimeout(function() {

        $('.regform')[0].addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
            }
        });

        ul = document.querySelector("ul");
        input = ul.querySelector("input");
        tagNumb = document.querySelector(".details span");
        

        countTags();
        createTag();
        input.addEventListener("keyup", addTag);

        input.addEventListener("keyup", addTag);
        const removeBtn = document.querySelector(".details button");
            removeBtn.addEventListener("click", () =>{
            tags.length = 0;
            ul.querySelectorAll("li").forEach(li => li.remove());
            countTags();
    });
    
    }, 1000);

    window.remove = function remove(element, tag) {
        let index  = tags.indexOf(tag);
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
        element.parentElement.remove();
        countTags();
    }

    function countTags() {
        input.focus();
        tagNumb.innerText = maxTags - tags.length;
    }

    function createTag() {
        ul.querySelectorAll("li").forEach(li => li.remove());
        tags.slice().reverse().forEach(tag =>{
            let liTag = `<li>${tag} <i class="uit uit-multiply" onclick="remove(this, '${tag}')"></i></li>`;
            ul.insertAdjacentHTML("afterbegin", liTag);
        });
        countTags();
    }

    
    function addTag(e){
        if(e.key == "Enter"){
            let tag = e.target.value.replace(/\s+/g, ' ');
            if(tag.length > 1 && !tags.includes(tag)){
                if(tags.length < 10){
                    tag.split(',').forEach(tag => {
                        tags.push(tag);
                        createTag();
                    });
                }
            }
            e.target.value = "";
        }
    }
}