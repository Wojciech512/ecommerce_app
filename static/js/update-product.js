  $(document).on('click', '.update-button', function(e){
    e.preventDefault();
    var theproductid = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: cartUpdateUrl,
        data: {
            product_id: $(this).data('index'),
            product_quantity: $('#select' + theproductid + ' option:selected').text(),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function(json){
            location.reload();
            document.getElementById("cart-qty").textContent = json.qty
            document.getElementById("total").textContent = json.total
        },
        error: function(xhr, errmsg, err){
            console.log("Error: ", errmsg);
        }
    });
})