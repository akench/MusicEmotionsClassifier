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
        $('#register-submit-btn').prop("disabled", true);
    } else {
        $('#passwd-not-match').hide(100);
        $('#register-submit-btn').prop("disabled", false);
    }
}


function checkEmailNotEmpty() {
    let email = $('#input-email').val()

    if (email === "") {
        $('#email-empty').show(100);
        $('#register-submit-btn').prop("disabled", true);
    } else {
        $('#email-empty').hide(100);
        $('register-submit-btn').prop("disabled", false);
    }
}



// we know the passwords must be different
function sendRegisterData() {

    let email = document.getElementById('input-email').value;
    let passwd = document.getElementById('input-password').value;

    let payload = { "email": email, "password": passwd };

    $.ajax({
        url: "http://localhost:5000/register",
        data: JSON.stringify(payload),
        method: "POST",
        contentType: "application/json",
        success: function (result) {

            if (result !== "0") {
                let msg = codeToStr[result];

                $('.alert').append(msg);
                $('.alert').show(100);
            }

        },
        error: function (err) {
            console.log(err);
        }
    });
}

