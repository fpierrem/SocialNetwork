// Load like, edit and delete controls for comments
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[id*="post_"]').forEach((element) => {
        likeControl(element,'post');
        editControl(element, 'post');
        deleteControl(element, 'post');
    });
})

