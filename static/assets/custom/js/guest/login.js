"use strict";
var SigninGeneral = function () { // Elements
    var form;
    var submitButton;
    var validator;



    var initializeFormValidation = function () {
        $("#_sign_in_form").validate({
			rules: {
                username: {
					required: true,
					minlength: 2,
                    email:true
				},
                password: {
					required: true,
					minlength: 3
				},
			},
			messages: {
                username: {
					required: "Please enter a username",
					minlength: "Your username must consist of at least 2 characters",
					email: "Please enter a valid email address"
				},
				password: {
					required: "Please provide a password",
					minlength: "Your password must be at least 3 characters long"
				},
				
			}
		});

    }

    // Handle form
    var handleForm = function (e) {

        // Handle form submit
        submitButton.addEventListener('click', function (e) { // Prevent button default action

            if($("#_sign_in_form").valid())
            {
                submitButton.disabled = false;
                e.preventDefault();


                let username = form.querySelector('[name="username"]').value
                let password = form.querySelector('[name="password"]').value

                $.post(`${api_config.login_url}`, {
                    email: username,
                    password: password
                }, function (data, status, xhr) {



                    if (data.status_code == 100) {
                        Swal.fire({
                            text: data.message,
                            icon: "success",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        }).then(function (result) {

                            if (result.isConfirmed) {
                                form.querySelector('[name="username"]').value = "";
                                form.querySelector('[name="password"]').value = "";

                                var redirectUrl = form.getAttribute('data-redirect-url');
                                if (redirectUrl) {
                                    location.href = redirectUrl;
                                }
                            }
                        });
                    } else {
                        Swal.fire({
                            text: data.message,
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }

                }, 'json').done(function () {
                    console.log('Request done!');
                }).fail(function (jqxhr, settings, ex) {
                    console.log('failed, ' + ex);
                });

            }
            


        });
    }

    // Public functions
    return { // Initialization
        init: function () {
            form = document.querySelector('#_sign_in_form');
            submitButton = document.querySelector('#_sign_in_submit');
            initializeFormValidation();
            handleForm();
        }
    };
}();

document.addEventListener("DOMContentLoaded", function() {
    SigninGeneral.init();
});