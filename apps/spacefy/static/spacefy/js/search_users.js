
document.addEventListener('DOMContentLoaded', function () {
    var searchbar = document.getElementById("searchbar");
    var resultDiv = document.getElementById('result');

    searchbar.addEventListener("input", function () {
            $.ajax({
                type: "GET",
                url: "/users-search/",
                data: {
                    "data": this.value
                },
                success: function (response) {
                    if (response["usernames"]){
                        for (let i = 0; i < response["usernames"].length; i++) {
                            console.log(response["usernames"][i]);
                        }
                        var listItems = response["usernames"].map(function (username) {
                        return '<a href="another-space/' + username + '/" style="text-decoration: none; color: #131314">' +
                            '<li>' + username + '</li>' + '</a>';}).join('');
                        resultDiv.innerHTML = '<ul>' + listItems + '</ul>';
                    } else {
                        resultDiv.innerHTML = '';
                    }
        },
                error: function (error) {
                    console.error("Error:", error)
                }
    })
    })
})
