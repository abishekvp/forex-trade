function csrfToken() {
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    return csrfToken;
}

function add_cart(product_id) {
    // Get CSRF token from meta tag
    $.ajax({
        type: "POST",
        url: "/client/add-cart",
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: csrfToken()
        },
        success: function (response) {
            if (response.status == 200) {
                alert(response.message);
            } else {
                if (response.message) {
                    alert(response.message);
                } else {
                    alert("Failed to add item to cart.");
                }
            }
        },
        error: function (xhr, status, error) {
            alert("An error occurred: " + error);
        }
    });
}