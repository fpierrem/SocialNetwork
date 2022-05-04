function deleteControl(element, target_type) {
    
    let target_id = target_type == 'post' ? element.id.substr(5) : element.id.substr(8);
    let delete_button = element.querySelector('#delete-button');
    
    if(delete_button){
        delete_button.addEventListener('click',show_modal);
    }
    
    function show_modal() {
        // Clone and replace delete modal to clear out potential event listeners from previous function calls
        var delete_modal = document.getElementById('delete-modal');
        var new_delete_modal = delete_modal.cloneNode(true);
        delete_modal.parentNode.replaceChild(new_delete_modal, delete_modal);

        // Display delete modal and add event listener for when delete button is clicked
        $('#delete-modal').modal('show');
        document.querySelector('#delete-confirm').addEventListener('click', delete_element);        

        function delete_element() {
            $('#delete-modal').modal('hide');
            fetch('/delete', {
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: JSON.stringify({
                    target_type: target_type,
                    target_id: target_id,
                })
            })
            .then(() => {
                if (element.className.includes('detailed-view')) {
                    window.location = '/';                 
                }
                else {
                element.parentNode.remove();
                }
            })
        }
    }
}

