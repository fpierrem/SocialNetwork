document.addEventListener('DOMContentLoaded', function() {
    followControl(document.querySelector('#follow-button'));
    imageModalControl()
})

// Handles clicks on follow/unfollow button and updates follower count accordingly
function followControl(element) {
    
    if (!element){
        return;
    }
    
    let profile_user_name = window.location.href.split('/').pop()
    
    element.addEventListener('click', event => {
        if (element.innerHTML == 'Follow') {
            // Create follow object
            fetch('/follow', {
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: JSON.stringify({
                    target: profile_user_name
                })
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
            })
            // Update follower count
            .then(update_followers(profile_user_name))
            // Switch button from Follow to Unfollow
            element.innerHTML = 'Unfollow'
            element.className = 'btn btn-secondary unfollow-button'
        }
        else if (element.innerHTML == 'Unfollow') {
            // Delete follow object
            fetch('/unfollow', {
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: JSON.stringify({
                    target: profile_user_name
                })
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
            })
            // Update follower count
            .then(update_followers(profile_user_name))
            // Switch button from unfollow to follow
            element.innerHTML = 'Follow'
            element.className = 'btn btn-primary follow-button'
        }
    })
    
    function update_followers(profile_user_name) {
        fetch(`${window.location.origin}/count_followers/${profile_user_name}`)
        .then(response => response.json())
        .then(count => {
            console.log(count);
            document.querySelector('#follower_count').innerHTML = `${count} follower${count>1?'s':''}`                
        })
    }
}

// Show modal with enlarged image when profile image is clicked on
function imageModalControl() {
    document.querySelector('#profile-image-large').addEventListener('click', () => {
        $('#profile-image-modal').modal('show')
    })
}