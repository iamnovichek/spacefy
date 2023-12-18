document.addEventListener("DOMContentLoaded", function () {
    let username = document.getElementById("uname")
        .getAttribute("data-username");
    let btn;
    try {
        btn = document.getElementById("add-to-friends");
        console.log(btn.value);
        console.log(btn.id);
        console.log(btn);
    } catch (error) {
        btn = document.getElementById("remove-from-friends");
        console.log(btn.value);
        console.log(btn.id);
        console.log(btn);
    }
    if (btn.id === "add-to-friends"){
        btn.addEventListener("click", function () {
        $.ajax({
                type: "POST",
                url: "/add-to-friends/" + username + "/",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $(':input[name="csrfmiddlewaretoken"]').val())
                },
                data: {
                    "username": username
                },
                success: function (result) {
                    console.log(result["result"]);
                    location.reload()
                },
                error: function (error) {
                    console.error("Error: ", error);
                }
            })
    });
    } else if (btn.id === "remove-from-friends") {
        btn.addEventListener("click", function () {
        $.ajax({
                type: "POST",
                url: "/remove-from-friends/" + username + "/",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", $(':input[name="csrfmiddlewaretoken"]').val())
                },
                data: {
                    "username": username
                },
                success: function (result) {
                    console.log(result["result"]);
                    location.reload()
                },
                error: function (error) {
                    console.error("Error: ", error);
                }
            })
    })
    }
})