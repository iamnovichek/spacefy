document.addEventListener("DOMContentLoaded", function () {
    let photos = Number(document.getElementById("data").
    getAttribute("data-to-grab"));
    var all_like_buttons = {};
    for (let i = 0; i < photos; i++) {
        all_like_buttons["like-" + (i+1)] = document.
        getElementById("like-" + (i+1))
    }
    for (const allLikeButtonsKey in all_like_buttons) {
        if (all_like_buttons[allLikeButtonsKey].getAttribute("data-liked")){
            all_like_buttons[allLikeButtonsKey].addEventListener('click', function () {
                $.ajax({
                type: "POST",
                url: "/like/",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $(':input[name="csrfmiddlewaretoken"]').val())
                },
                data: {
                    "type": "photo",
                    "gallery_id": document.getElementById(allLikeButtonsKey).
                    getAttribute("data-gallery-id")
                },
                success: function (result) {
                    location.reload();
                    console.log(result["result"])
                }
            })
            })
        } else {
            $.ajax({
                type: "POST",
                url: "/unlike/",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $(':input[name="csrfmiddlewaretoken"]').val())
                },
                data: {
                    "type": "photo",
                    "gallery_id": document.getElementById(allLikeButtonsKey).
                    getAttribute("data-gallery-id")
                },
                success: function (result) {
                    location.reload();
                    console.log(result["result"])
                }
            })
        }
    }

})