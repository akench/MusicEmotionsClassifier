

(function () {

    $(document).ready(function () {

        // initially tells you that email is empty, since it is
        checkEmailNotEmptyLogin();
        checkEmailNotEmptyRegister();

        // same for password
        checkPasswordNotEmptyLogin();
        checkPasswordNotEmptyRegister();

        // click register btn
        $('#register-submit-btn').on('click', sendRegisterData);

        // click login btn
        // TODO hi

        // do passwords match for registering?
        $('#input-password-reg, #input-confirm-password-reg').on('change keyup mouseup', checkPasswordsMatch);
       
        // did you leave any password fields blank?
        $('#input-password-reg, #input-confirm-password-reg').on('change keyup mouseup', checkPasswordNotEmptyRegister);
        $('#input-password-login').on('change keyup mouseup', checkEmailNotEmptyLogin);

        // did you leave any email fields blank?
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


    function checkPasswordNotEmptyRegister() {

        let pass = $('#input-password-reg').val();
        let confirmPass = $('#input-confirm-password-reg').val();

        if(pass === "" || confirmPass == "") {
            $('#passwd-empty-register').show(100);
            $('#register-submit-btn').prop("disabled", true);
        } else {
            $('#passwd-empty-register').hide(100);
            $('#register-submit-btn').prop("disabled", false);
        }
    }


    function checkPasswordNotEmptyLogin() {
        
        let pass = $('#input-password-login').val();

        if(pass === "") {
            $('#passwd-empty-login').show(100);
            $('#login-submit-btn').prop("disabled", true);
        } else {
            $('#passwd-empty-login').hide(100);
            $('#login-submit-btn').prop("disabled", false);
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


    function sendLoginData() {

        let email = $('#input-email-login').val();
        let passwd = $('input-password-login').val();

        let payload = { "email": email, "password": passwd };

        $.ajax({
            url: "http://localhost:5000/login",
            data: JSON.stringify(payload),
            method: "POST",

            success: function (data) {

            },
            error: function (err) {

            }
        })
    }


})();



