$("span[class*=star-rating-span-]").each((key, element) => {
    var rating = $(element).attr("class").replace("star-rating-span-", "");
    $(element).html('<i class="fa fa-star star-yellow"></i>'.repeat(rating));
})