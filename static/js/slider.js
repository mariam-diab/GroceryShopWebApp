$(function() {
    var minValue = parseInt($(".price-range").attr("data-min"));
    var maxValue = parseInt($(".price-range").attr("data-max"));
    
    function initializeSlider() {
        $(".price-range").slider({
            range: true,
            min: minValue,
            max: maxValue,
            values: [minValue, maxValue],
            slide: function(event, ui) {
                $("#minamount").val(ui.values[0]);
                $("#maxamount").val(ui.values[1]);
                delayedRedirect();
            }
        });
    }

    initializeSlider();

    function updateInputValues() {
        var minVal = $(".price-range").slider("values", 0);
        var maxVal = $(".price-range").slider("values", 1);
        $("#minamount").val(minVal);
        $("#maxamount").val(maxVal);
    }

    updateInputValues();

    function redirectToShopGrid() {
        var minAmount = $("#minamount").val();
        var maxAmount = $("#maxamount").val();
        console.log("Slider values:", minAmount, maxAmount);

        var url = "{% url 'GroceryApp:shop_grid' %}?minamount=" + minAmount + "&maxamount=" + maxAmount;
        var url = "/shop_grid/?minamount=" + minAmount + "&maxamount=" + maxAmount;
        window.location.href = url;
    }

    var delayTimer;
    function delayedRedirect() {
        clearTimeout(delayTimer);
        delayTimer = setTimeout(redirectToShopGrid, 500);
    }

    $("#minamount, #maxamount").on("input", redirectToShopGrid);
});
