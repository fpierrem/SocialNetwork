document.addEventListener('DOMContentLoaded', function() {
    post_button = document.querySelector('#post-button');
    if(post_button) {
        post_button.addEventListener('click', new_post);
    }
})

function new_post() {

    // Get post text from textarea
    const post_text = document.querySelector('#new-post').value;

    // Send POST request to post API route
    fetch('/write_post', {
        method: 'POST',
        headers: {"X-CSRFToken": csrftoken},
        body: JSON.stringify({
            text: post_text
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    // Reload the page to display the new post and clear out the new post textarea
    window.location.reload(true);
}