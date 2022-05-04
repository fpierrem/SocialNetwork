// Load like, edit and delete controls for comments
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[id*="comment_"]').forEach((element) => {
        likeControl(element,'comment');
        editControl(element, 'comment');
        deleteControl(element, 'comment');
    });
})

