function file_validation() {
    var file_input = document.getElementById('user-photo')
    var file_path = file_input.value
    var allowed_extensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i
    if (!allowed_extensions.exec(file_path)) {
        alert('Invalid file type');
        file_input.value = '';
        return false;
    }
    if (file_input.files[0].size > 1024 * 1024) {
        alert('Image is too big. Max size is 1 Mb');
        file_input.value = '';
        return false;
    }
}
