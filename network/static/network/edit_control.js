function editControl(element, target_type) {
    
    let target_id = target_type == 'post' ? element.id.substr(5) : element.id.substr(8);
    let edit_button = element.querySelector('#edit-button');

    if(edit_button){
        edit_button.addEventListener('click',show_modal);
    }

    function show_modal() {
        // Clone and replace edit modal to clear out potential event listeners from previous function calls
        var edit_modal = document.getElementById('edit-modal');
        var new_edit_modal = edit_modal.cloneNode(true);
        edit_modal.parentNode.replaceChild(new_edit_modal, edit_modal);

        // Display edit modal, fill in text area and add event listener to submit button
        $('#edit-modal').modal('show');
        document.querySelector('#text-to-edit').innerHTML = element.querySelector(`#${target_type}-text`).innerHTML;        
        document.querySelector('#edit-submit').addEventListener('click', edit);        

        function edit() {
            edited_text = document.querySelector('#text-to-edit').innerHTML;
            fetch('/edit', {
                method: 'POST',
                headers: {"X-CSRFToken": csrftoken},
                body: JSON.stringify({
                    target_type: target_type,
                    target_id: target_id,
                    edited_text: edited_text
                })
            })
            element.querySelector(`#${target_type}-text`).innerHTML = edited_text;
            if(!element.querySelector(`#${target_type}-timestamp`).innerHTML.includes(' · Edited')) {
                element.querySelector(`#${target_type}-timestamp`).innerHTML += ' · Edited';
            }
        }
    }
}

