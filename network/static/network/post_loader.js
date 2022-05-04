document.addEventListener('DOMContentLoaded', () => {    
    // context determines which users' posts should be loaded     
    let context = 'all_users';
    if (window.location.href.split('/').pop() == 'following') {
        context = 'followed_users';
    }
    if (window.location.href.includes('profile')) {
        context = window.location.href.split('/').pop();
    }
    // load new batch of posts whenever sentinel at bottom of page becomes visible     
    let sentinel = document.getElementById("sentinel");
    let counter = 0;
    let observer = new IntersectionObserver(entries => {
        entry = entries[0];
        if (entry.isIntersecting) {
            counter += 1;
            load(counter, context);
        }
    }, options = {rootMargin: "1px"})
    observer.observe(sentinel);
})

function load(counter, context) {
    fetch(`/posts?page=${counter}&context=${context}`)
    .then(response => {
        // console.log(response)
        if (response.ok) {
            return response.text(); 
        }
        else {
            return "";
        }
    })
    .then (data => {
        if (context == 'followed_users' && data == "") {
            document.querySelector('#posts').innerHTML = 
            `<div class="container posts-container">
            <div>You are not following anyone.</div>`;
        }
        document.querySelector('#posts').innerHTML += data;
    })
    .then(response => {
        load_controls()
    })
}

function load_controls() {
    document.querySelectorAll('[id*="post_"]').forEach((element) => {
        likeControl(element,'post');
        editControl(element, 'post');
        deleteControl(element, 'post');
    })
}

