function submitURL(event) {

    let url = event.data.val();

    $.ajax({
        url: "http://localhost:5000/classify",
        method: "POST",
        data: JSON.stringify({ "url": url }),
        contentType: "application/json",
        success: function (result) {
            alert(result);
        },
        error: function (err) {
            alert(err.statustext);
        }
    });

}


function checkPasswordsMatch() {

    let pass = $('#input-password').val();
    let confirmPass = $('#input-confirm-password').val();

    if (pass !== confirmPass) {
        $('#passwd-not-match').show(100);
    } else {
        $('#passwd-not-match').hide(100);
    }

}


function sendRegisterData() {


}

