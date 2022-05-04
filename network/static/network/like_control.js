function likeControl(element,target_type) {
    
    let target_id = target_type == 'post' ? element.id.substr(5) : element.id.substr(8);
    let button = element.querySelector('#like-button');
    let icon = element.querySelector('#like-icon');
    let counter = element.querySelector('#like-counter');

    update_like_count();

    // Update like status only if user is logged in (if log out link is displayed)
    let log_out_link = document.querySelector('#log-out-link');
    if(log_out_link) {
        check_like_status();
    }

    function check_like_status() {
        fetch(`/check_like_status?target_type=${target_type}&target_id=${target_id}`)
        .then(response => response.json())
        .then(liked => {
            // console.log(liked);
            update_like_button(liked);
            if (liked) {
                button.addEventListener('click',unlike)
            }
            else {
                button.addEventListener('click',like)
            }
        })
    }

    function update_like_count() {
        fetch(`/count_likes?target_type=${target_type}&target_id=${target_id}`)
        .then(response => response.json())
        .then(c => {
            counter.innerHTML = c;
        })
    }

    function update_like_button(liked) {
        icon.className = liked ? 'fas fa-heart' : 'far fa-heart';
        icon.style.color = liked ? "red" : "grey";
    }

    function like() {
        // call like API, change icon, update like count and change click event to unlike
            fetch(`${window.location.origin}/like`,{
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: JSON.stringify({
                    target_type: target_type,
                    target_id: target_id
                })
            })
            .then(update_like_count())
            button.removeEventListener('click',like)
            button.addEventListener('click',unlike)
            update_like_button(true)
        }

    function unlike() {
    // call unlike API, change icon and update like count and change click event to like
        fetch(`${window.location.origin}/unlike`,{
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({
                target_type: target_type,
                target_id: target_id
            })
        })
        .then(update_like_count())
        button.removeEventListener('click',unlike)
        button.addEventListener('click',like)
        update_like_button(false)
    }
}

