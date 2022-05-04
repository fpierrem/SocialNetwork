document.addEventListener('DOMContentLoaded', function() {
    comment_button = document.querySelector('#write-comment-button');
    if(comment_button) {
        comment_button.addEventListener('click', commentControl);
    }
})

function commentControl(element) {    
        const post_id = window.location.href.split('/post/').pop();
        const comment_text_area = document.getElementById('comment-text-area');
        const comment_text = comment_text_area.value;

        fetch('/write_comment', {
            method: 'POST',
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({
                post_id: post_id,
                text: comment_text
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })

        // Clear text area
        comment_text_area.innerHTML = "";

        // Reload page or add new comment to comment list and update comment count
        location.reload(true);
}