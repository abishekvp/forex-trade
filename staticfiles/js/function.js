const POST = 'post'
const GET = 'get'
const PUT = 'put'
const DELETE = 'delete'

function notify(response){
    console.log(response);
    var message = response['message'];
    var status_code = response['status_code'];
    $('#notify-alert-message').removeClass('d-none');
    $('#notify-alert-message').addClass('d-block');
    $('#notify-message').text(message);
    setTimeout(function() {
        $('#notify-alert-message').removeClass('d-block');
        $('#notify-alert-message').addClass('d-none');
    }, 5000);    
}

function getInputFIeldsData(id) {
    const fieldsDiv = document.getElementById(id);
    const inputs = fieldsDiv.querySelectorAll('input, select');
    const inputData = {};
    let hasFiles = false;

    inputs.forEach(input => {
        const input_name = input.name;
        const input_id = input.id;
        let input_value;
        if (!inputData[input_name]) {
            inputData[input_name] = [];
        }
        if (input.type === 'file') {
            if (input.files.length > 0) {
                input_value = input.files[0];
                hasFiles = true;
            }
        } 
        else if (input.type === 'checkbox' || input.type === 'radio') {
            if (input.checked) {
                input_value = input.value;
            }
        } 
        else {
            input_value = input.value;
        }
        if (input_value !== undefined) {
            const fieldInput = { [input_id]: input_value };
            inputData[input_name].push(fieldInput);
        }
    });
    return { inputData, hasFiles };
}

function getProductFieldsData(id) {
    const fieldsDiv = document.getElementById(id);
    const inputs = fieldsDiv.querySelectorAll('input, select');
    const inputData = {};
    let hasFiles = false;

    inputs.forEach(input => {
        const input_name = input.name;
        const input_id = input.id;
        let input_value;
        if (!inputData[input_name]) {
            inputData[input_name] = [];
        }
        if (input.type === 'file') {
            if (input.files.length > 0) {
                input_value = input.files[0];
                hasFiles = true;
            }
        } 
        else if (input.type === 'checkbox' || input.type === 'radio') {
            if (input.checked) {
                input_value = input.value;
            }
        } 
        else {
            input_value = input.value;
        }
        if (input_value !== undefined) {
            const fieldInput = { [input_id]: input_value };
            inputData[input_name].push(fieldInput);
        }
    });
    return { inputData, hasFiles };
}

function raise_request(url, method, data, hasFiles = false, callback) {
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    const contentType = hasFiles ? false : 'application/json';
    let payload = hasFiles ? new FormData() : JSON.stringify(data);

    if (hasFiles) {
        payload.append('data', data);
    }
    
    $.ajax({
        url: url,
        type: method,
        data: method !== 'GET' ? {
            'csrfmiddlewaretoken': csrfToken,
            'data': payload
        } : null,
        success: function(response) {
            callback(response);
        },
        error: function(error) {
            callback(null, error);
        }
    });
}

function get_fields() {
    raise_request('/get-fields', 'GET', {}, false, function(response, error) {
        if (error) {
            console.error("Error:", error);
            return;
        }
        var data = response.fields;
        const container = document.getElementById('add-product-fields');
        
        data.forEach(field => {
            const div = document.createElement('div');
            div.className = 'col-md-12';
            div.innerHTML = `
                <input 
                    type="${field.type.field_type}"
                    name="${field.name}"
                    id="${field.input_id}"
                    class="form-control ${field.input_class}"
                    placeholder="${field.placeholder}"
                    ${field.properties.map(property => property.value ? `${property.tag}="${property.value}"` : property.tag).join(' ')}
                >
                if (field.type.field_type === 'checkbox") {
                    div.innerHTML += `
                        <label for="${field.input_id}" class="form-check-label">${field.label}</label>
                    `;
                }
            `;
            container.appendChild(div);
        });
    });
}

function add_field(){
    const { inputData, hasFiles } = getInputFIeldsData('modalAddField');
    var response = raise_request('/add-field', POST, inputData, hasFiles);
    notify(response);
}

function add_image(url, method, data){
    var formData = new FormData();

    for (var key in data) {
        formData.append(key, data[key]);
    }

    formData.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());

    $.ajax({
        url: url,
        type: method,
        data: formData,
        processData: false,  // Important!
        contentType: false,  // Important!
        success: function (response) {
            return response;
        },
        error: function (error) {
            console.log(error);
            return error;
        }
    });
}

function add_product(){
    const { inputData, hasFiles } = getInputFIeldsData('modalAddProduct');
    var response = raise_request('/add-product', 'POST', inputData, hasFiles);
    notify(response);
}

function add_product_image(){
    var fileInput = $('#product-image')[0];
    var file = fileInput.files[0];
    raise_request('/add-product-image', 'POST', { 'product-image': file });
}

function delete_field(field_id){
    var response = raise_request('/delete-field', POST, {'field-id': field_id});
}

function add_property(){
    var response = raise_request('/add-property', POST, {
        'property-name': $('#property-name').val(),
        'property-tag': $('#property-tag').val(),
        'property-value': $('#property-value').val(),
        'property-type': $('#property-type').val(),
        'property-description': $('#property-description').val()
    })
    notify(response);
}

function add_input_type(){
    var response = raise_request('/add-input-type', POST, {
        'input-type-name': $('#input-type-name').val(),
        'input-type-value': $('#input-type-value').val(),
    })
}