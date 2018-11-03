function submitURL() {

    let url = document.getElementById("url-box").value;

    $.ajax({
        url: "http://localhost:5000/classify",
        method: "POST",
        data: JSON.stringify({"url": url}),
        contentType: "application/json",
        success: function(result) {
            alert(result);
        },
        error: function(err) {
            alert(err.statustext);
        }
    });

}