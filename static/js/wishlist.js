$(document).on("click", ".make-default-address", function() {
    let id = $(this).attr("data-address-id");
    let this_val = $(this);
    console.log("ID is:", id);
    console.log("Element is:", this_val);
    $.ajax({
        url: "/make-default-address",
        data: {
            "id": id
        },
        dataType: "json",
        success: function(response) {
            console.log("Address Made Default....");
            if (response.boolean == true) {
                $(".check").hide();
                $(".action_btn").show();
                $(".check" + id).show();
                $(".button" + id).hide();
            }
        }
    });
});

// Adding to wishlist
$(document).on("click", ".add-to-wishlist", function() {
    let product_id = $(this).attr("data-product-item");
    let this_val = $(this);
    console.log("Product ID IS", product_id);
    $.ajax({
        url: "/add-to-wishlist",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function() {
            console.log("before send")
            this_val.html("/");
        },
        success: function(response) {
            if (response.bool ===True){
                console.log("added خرا")
            }
        }
    });
});

