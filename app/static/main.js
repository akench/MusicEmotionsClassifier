

(function () {

    $(document).ready(function () {

        // initially tells you that email is empty, since it is
        checkEmailNotEmptyLogin();
        checkEmailNotEmptyRegister();

        $('#register-submit-btn').on('click', sendRegisterData);

        $('#input-password-reg, #input-confirm-password-reg').on('change keyup mouseup', checkPasswordsMatch);

        $('#input-email-reg').on('change keyup mouseup', checkEmailNotEmptyRegister);

        $('#input-email-login').on('change keyup mouseup', checkEmailNotEmptyLogin);

        // set up click listener to send url to server
        // let urlbox = $("#url-box");
        // $("#submit-url").on('click', urlbox, submitURL);

    });


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

    function checkEmailNotEmptyRegister(keyevent) {
        let email = (keyevent) ? keyevent.target.value : "";

        if (email === "") {
            $('#email-empty-register').show(100);
            $('#register-submit-btn').prop("disabled", true);
        } else {
            $('#email-empty-register').hide(100);
            $('#register-submit-btn').prop("disabled", false);
        }
    }


    function checkPasswordsMatch() {

        let pass = $('#input-password-reg').val();
        let confirmPass = $('#input-confirm-password-reg').val();

        if (pass !== confirmPass) {
            $('#passwd-not-match').show(100);
            $('#register-submit-btn').prop("disabled", true);
        } else {
            $('#passwd-not-match').hide(100);
            $('#register-submit-btn').prop("disabled", false);
        }
    }



    function checkEmailNotEmptyLogin(keyevent) {
        let email = (keyevent) ? keyevent.target.value : "";

        if (email === "") {
            $('#email-empty-login').show(100);
            $('#login-submit-btn').prop("disabled", true);
        } else {
            $('#email-empty-login').hide(100);
            $('#login-submit-btn').prop("disabled", false);
        }
    }



    // we know the passwords must be different
    function sendRegisterData() {

        let email = document.getElementById('input-email-reg').value;
        let passwd = document.getElementById('input-password-reg').value;

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


    function sendLoginData() {

        let email = $('#input-email-login').val();
        let passwd = $('input-password-login').val();

        let payload = { "email": email, "password": passwd };

        $.ajax({
            url: "http://localhost:5000/login",
            data: JSON.stringify(payload),
            method: "POST",
            
            success: function(data) {

            },
            error: function(err) {

            }
        })
    }


})();



