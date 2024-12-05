$(document).on('click', '#add-button', function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: cartAddUrl,
        data: {
            product_id: $('#add-button').val(),
            product_quantity: $('#select option:selected').text(),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function(json) {
            document.getElementById("cart-qty").textContent = json.qty;
        },
        error: function(xhr, errmsg, err) {
            console.log("Error: ", errmsg);
        }
    });
});
