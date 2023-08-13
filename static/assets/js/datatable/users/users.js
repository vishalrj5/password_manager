"use strict";

// Class definition
var KTDatatablesServerSide = function() {
    // Shared variables
    var table;
    var dt;

    // Private functions
    var initDatatable = function() {

        dt = $("#users-datatable").DataTable({
            searchDelay: 500,
            serverSide: true,
            responsive: true,
            processing: true,
            order: [
                [1, 'desc']
            ],
            ajax: {
                method: "GET",
                url: `${api_config.datatable}`,
                data: {
                },
            },
            columns: [
                {data: 'id'},
                {data: 'image'},
                {data: 'email'},
                {data: 'first_name'},
                {data: 'last_name'},
                {data: 'is_active'},
                {data: 'id'},
            ],
            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, row) {
                        return `
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input checkbox-input-id" type="checkbox" value="${data}" />
                            </div>`;
                    }
                },
                {
                    targets: 1,
                    orderable: false,
                    render: function (data, type, row) {
                        return `<span class="user-img-wrap">
                                <img
                                src="${row.image}"
                                class="img-fluid"
                                style="width: 50px; height: 50px; border-radius: 50%;"
                                />
                            </span>`;
                    }
                },
                {
                    targets: 2,
                    orderable: false,
                    render: function (data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.id.toString());
                        return `<a href="${edit_url}" >${data}</a>`;
                    }
                },
                
                {
                    targets: 5,
                    orderable: false,
                    render: function (data, type, row) {
                        let label = '';
                        if(data)
                        {
                            label = `<span class="status green">Verified</span>`
                        }else{
                            label = `<span class="status red">Pending</span>`
                        }
                        return label;
                    }
                },
                {
                    targets: -1,
                    orderable: false,
                    render: function (data, type, row) {
                        return `<button data-id=${row.id} data-users-table-filter="delete_row" class="btn btn-danger" style="min-width: 0;padding: 6px;"><i class="fa fa-trash" aria-hidden="true"></i></button>`;
                    }
                },
            ],
            // Add data-filter attribute
            drawCallback: function(settings) {},
            createdRow: function(row, data, dataIndex) {
                $(row).find('td:eq(4)').attr('data-filter', data.CreditCardType);
            }
        });

        table = dt.$;
        dt.on('draw', function() {
            handleDeleteRows();
        });
    }



    // Delete users
    var handleDeleteRows = () => {
        // Select all delete buttons
        const deleteButtons = document.querySelectorAll('[data-users-table-filter="delete_row"]');

        deleteButtons.forEach(d => {
            // Delete button on click
            d.addEventListener('click', function(e) {

                const destroyRecordIds = [$(this).data('id')];
                e.preventDefault();
                // Select parent row
                const parent = e.target.closest('tr');
                // Get customer name
                const userName = parent.querySelectorAll('td')[3].innerText +' '+parent.querySelectorAll('td')[4].innerText;

                //     // SweetAlert2 pop up --- official docs reference: https://sweetalert2.github.io/
                Swal.fire({
                    text: "Are you sure you want to delete " + userName + "?",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: false,
                    confirmButtonText: "Yes, delete!",
                    cancelButtonText: "No, cancel",
                    customClass: {
                        confirmButton: "btn fw-bold btn-danger",
                        cancelButton: "btn fw-bold btn-active-light-primary"
                    }
                }).then(function(result) {
                    if (result.value) {
                        $.post(`${api_config.delete_records}`, { ids: destroyRecordIds, 'csrfmiddlewaretoken': `${api_config.csrfmiddlewaretoken}` }, function(data, status, xhr) {

                            if (data.status_code = 200) {
                                Swal.fire({
                                    text: "You have deleted " + userName + "!.",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                }).then(function() {
                                    // delete row data from server and re-draw datatable
                                    dt.draw();
                                });

                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }

                        }, 'json').done(function() {
                            console.log('Request done!');
                        }).fail(function(jqxhr, settings, ex) {
                            console.log('failed, ' + ex);
                            Swal.fire({
                                text: "Something went wrong.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            });
                        });

                    } else if (result.dismiss === 'cancel') {
                        Swal.fire({
                            text: groupName + " was not deleted.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-primary",
                            }
                        });
                    }
                });
            })
        });
    }
    


    // Public methods
    return {
        init: function() {
            initDatatable();
            handleDeleteRows();
        }
    }
}();

// On document ready
document.addEventListener("DOMContentLoaded", function() {
    KTDatatablesServerSide.init();
});