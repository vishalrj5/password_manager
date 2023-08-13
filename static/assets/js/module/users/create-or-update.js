"use strict";

// Class definition
var createUser = function() {
    // Shared variables

    // Private functions
    var initializeFormValidation = function() {
        $("#__create_or_update_users_form").validate({
            errorClass: "validation-error",
			rules: {
                email: {
					required: true,
                    email:true
				},
                username: {
					required: true,
					minlength: 2,
				},
                first_name: {
					required: true,
					minlength: 3
				},
                last_name: {
					required: true,
					minlength: 3
				},
                phone: {
					required: true,
					minlength: 10,
                    maxlength: 10,
                    digits:true,
				},
                gender: {
					required: true,
				},
                
			},
			messages: {
                email: {
					required: "Please enter a email",
					email: "Please enter a valid email address"
				},
                username: {
					required: "Please enter a username",
					minlength: "Your username must consist of at least 2 characters",
					email: "Please enter a valid email address"
				},
				first_name: {
					required: "Please enter a first_name",
					minlength: "Your first_name must be at least 3 characters long"
				},
                last_name: {
					required: "Please enter a last_name",
					minlength: "Your last_name must be at least 3 characters long"
				},
                phone: {
					required: "Please enter a phone",
					minlength: "Your phone must be at least 10 characters long"
				},
                gender: {
					required: "Please enter a gender",
				},
				
			},
            highlight: function ( element, errorClass, validClass ) {
                $( element ).next( "input" ).addClass( "inputvalidation-error" );
              }
		});

    }


    var onValidate = function() {
        if($("#__create_or_update_users_form").valid())
        {
            return true;
        }else{
            return false;
        }
    }

    
    


    // Public methods
    return {
        init: function() {
            initializeFormValidation();
        }
    }
}();

// On document ready
document.addEventListener("DOMContentLoaded", function() {
    createUser.init();
});