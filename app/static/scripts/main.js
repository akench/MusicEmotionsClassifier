

(function () {

    $(document).ready(function () {

        // do some initial input verf
        inputVerificationLogin()
        inputVerificationRegister()

        // click register btn
        $('#register-submit-btn').on('click', sendRegisterData);


        // verify input for register pg
        $('#input-email-reg, #input-password-reg, #input-confirm-password-reg').on('change keyup mouseup', inputVerificationRegister);

        // verify input for login pg
        $('#input-email-login, #input-password-login').on('change keyup mouseup', inputVerificationLogin);


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


    function inputVerificationRegister() {

        let email = $('#input-email-reg').val();
        let pass = $('#input-password-reg').val();
        let confPass = $('#input-confirm-password-reg').val();

        let emailBlank = (email === "");
        let passBlank = (pass === "" || confPass === "");
        let passNotMatch = (pass !== confPass);

        // if there is some problem disable the button
        if (emailBlank || passBlank || passNotMatch) {

            // if email is blank
            if (emailBlank) {
                $('#email-empty-register').show(100);
            } else {
                $('#email-empty-register').hide(100);
            }
            // if either password is blank
            if (passBlank) {
                $('#passwd-empty-register').show(100);
            } else {
                $('#passwd-empty-register').hide(100);
            }
            // if passwords dont match and neither are blank
            if (passNotMatch && !passBlank) {
                $('#passwd-not-match').show(100);
            } else {
                $('#passwd-not-match').hide(100);
            }

            $('#register-submit-btn').prop("disabled", true);
        } else {
            // if no problems, hide everything and enable btn
            $('#email-empty-register').hide(100);
            $('#passwd-empty-register').hide(100);
            $('#passwd-not-match').hide(100);

            $('#register-submit-btn').prop("disabled", false);
        }
    }

    function inputVerificationLogin() {
        let email = $('#input-email-login').val();
        let pass = $('#input-password-login').val();

        let emailBlank = (email === "");
        let passBlank = (pass === "");

        // if there is some problem disable the button
        if (emailBlank || passBlank) {

            // if email is blank
            if (emailBlank) {
                $('#email-empty-login').show(100);
            } else {
                $('#email-empty-login').hide(100);
            }
            // if password is blank
            if (passBlank) {
                $('#passwd-empty-login').show(100);
            } else {
                $('#passwd-empty-login').hide(100);
            }

            $('#login-submit-btn').prop("disabled", true);
        } else {
            // if no problems, hide everything and enable btn
            $('#email-empty-login').hide(100);
            $('#passwd-empty-login').hide(100);

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

                    // remove any success alerts, if there are any
                    $('.alert-success').slideUp("fast");

                    $('.alert-danger').empty();
                    $('.alert-danger').slideUp("fast");
                    $('.alert-danger').append(msg);
                    $('.alert-danger').slideDown("slow");
                } else {

                    // remove any error alerts, if there are any
                    $('.alert-danger').slideUp("fast");

                    $('.alert-success').empty();
                    $('.alert-success').slideUp("fast");
                    $('.alert-success').append("You have successfully registered. Please log in.")
                    $('.alert-success').slideDown("slow");

                    // switches to login tab
                    $('#login-tab-btn').trigger("click");

                }

            },
            error: function (err) {
                console.log(err);

                // remove any success alerts, if there are any
                $('.alert-success').slideUp("fast");

                $('.alert-danger').empty();
                $('.alert-danger').slideUp("fast");
                $('.alert-danger').append("There was an unknown error. Please try again later");
                $('.alert-danger').slideDown("slow");

            }
        });
    }



})();



