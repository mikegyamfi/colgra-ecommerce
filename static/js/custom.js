$(document).ready(function () {
  $(".inc-btn").click(function (e) {
    e.preventDefault();

    let inc_value = $(this.closest(".product-data")).find(".qty-val").val();
    let value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;

    if (value < 10) {
      value++;
      $(this.closest(".product-data")).find(".qty-val").val(value);
    }
  });

  $(".dec-btn").click(function (e) {
    e.preventDefault();

    let inc_value = $(this.closest(".product-data")).find(".qty-val").val();
    let value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;

    if (value > 1) {
      value--;
      $(this.closest(".product-data")).find(".qty-val").val(value);
    }
  });

  $(".addToCart").click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var product_qty = $(this).closest(".product-data").find(".qty-val").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/add-to-cart/",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });

  $(".changeQty").click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var product_qty = $(this).closest(".product-data").find(".qty-val").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/update-cart",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });

  $(".addtoWishlist").click(function (e) {
    e.preventDefault();

    let product_id = $(this).closest(".product-data").find(".prod_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/add-to-wishlist/",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
    });
  });

  $(".addtoWishlistfrommain").click(function (e) {
    e.preventDefault();

    let product_id = $(this).closest(".product-data").find(".prod_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/add-to-wishlist/",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".collection-product-data").load(
          location.href + " .collection-product-data"
        );
      },
    });
  });

  $(document).on("click", ".submit-review", function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var comment_text = $(".review-textarea").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/add-comment/",
      data: {
        product_id: product_id,
        comment_text: comment_text,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".comment-data").load(location.href + " .comment-data");
      },
    });
    $(".review-textarea").val("");
  });

  $(document).on("click", ".delete-cart-item", function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/delete-cart-item",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".cart_data").load(location.href + " .cart_data");
      },
    });
  });

  $(document).on("click", ".delete-comment", function (e) {
    e.preventDefault();

    var comment_id = $(this).closest(".product-data").find(".comment_id").val();
    console.log(comment_id);
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/delete-comment/",
      data: {
        comment_id: comment_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".comment-data").load(location.href + " .comment_data");
      },
    });
  });

  $(document).on("click", ".delete-wishlist-item", function (e) {
    e.preventDefault();

    let product_id = $(this).closest(".product-data").find(".prod_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/delete-wishlist-item",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".wishlist_data").load(location.href + " .wishlist_data");
      },
    });
  });

  $(document).on("click", ".delete-wishlist-item-from-main", function (e) {
    e.preventDefault();

    let product_id = $(this).closest(".product-data").find(".prod_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/delete-wishlist-item",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".collection-product-data").load(
          location.href + " .collection-product-data"
        );
      },
    });
  });
});
