    $(document).on('click', '.delete-button', function(e){
      e.preventDefault();
      $.ajax({
          type: 'POST',
          url: cartDeleteUrl,
          data: {
              product_id: $(this).data('index'),
              csrfmiddlewaretoken: csrfToken,
              action: 'post'
          },
          success: function(json){
              location.reload();
              document.getElementById("cart-qty").textContent = json.qty
              document.getElementById("total").textContent = json.total
          },
          error: function(xhr, errmsg, err){
          }
      });
  })