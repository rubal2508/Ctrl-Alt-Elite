function equalizeCardHeights() {
    var maxCardHeight = 0;
    $(".card").each((idx, element) => {
        maxCardHeight = Math.max(maxCardHeight, $(element).height());
    });

    $(".card").css("height", `${maxCardHeight}px`);
}

$(document).ready(function () {
    equalizeCardHeights();
})