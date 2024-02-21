$(document).ready(function() {
    // Function to fetch total expenses
    function fetchTotalExpenses() {
        $.ajax({
            url: '/total_expenses', // Assuming this route exists in your Flask app
            type: 'GET',
            success: function(response) {
                $('#total-expenses-value').text(response.total_expenses);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching total expenses:', error);
            }
        });
    }

    // Function to handle adding expense
    $('#expense-form').submit(function(event) {
        event.preventDefault();
        var amount = $('#amount').val();
        var description = $('#description').val();
        var store = $('#store').val();
        $.ajax({
            url: '/add_expense',
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            data: {amount: amount, description: description, store: store},
            success: function(response) {
                console.log('Expense added successfully:', response);
                location.reload();
            },
            error: function(xhr, status, error) {
                console.error('Error adding expense:', error);
            }
        });
    });

    function editExpense(expenseId) {
        // Send a GET request to fetch the expense details
        $.ajax({
            url: '/get_expense/' + expenseId,
            type: 'GET',
            success: function(response) {
                // Populate the edit form with the fetched expense details
                $('#edit-amount').val(response.amount);
                $('#edit-description').val(response.description);
                $('#edit-store').val(response.store_id); // Set the selected store id

                // Fetch stores to populate the dropdown
                $.ajax({
                    url: '/get_stores',
                    type: 'GET',
                    success: function(stores) {
                        // Populate the store dropdown with options
                        $('#edit-store').empty();
                        $.each(stores, function(index, store) {
                            $('#edit-store').append('<option value="' + store.id + '">' + store.name + '</option>');
                        });

                        // Show the edit modal
                        $('#editExpenseModal').modal('show');
                    },
                    error: function(xhr, status, error) {
                        console.error('Error fetching stores:', error);
                    }
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching expense details:', error);
            }
        });
    }

    // Function to handle editing expense
    $('#editExpenseForm').submit(function(event) {
        event.preventDefault();
        var expenseId = $('#edit-expense-id').val();
        var amount = $('#edit-amount').val();
        var description = $('#edit-description').val();
        var store = $('#edit-store').val();
        $.ajax({
            url: '/edit_expense/' + expenseId,
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded',
            data: {amount: amount, description: description, store: store},
            success: function(response) {
                console.log('Expense updated successfully:', response);
                // Fetch total expenses after editing an expense
                fetchTotalExpenses();
                window.location.href = '/';  // Redirect to the index page after editing
            },
            error: function(xhr, status, error) {
                console.error('Error updating expense:', error);
            }
        });
    });

    // Function to handle deleting expense
    function deleteExpense(expenseId) {
        if (confirm('Are you sure you want to delete this expense?')) {
            $.ajax({
                url: '/delete_expense/' + expenseId,
                type: 'DELETE',
                success: function(response) {
                    console.log('Expense deleted successfully:', response);
                    // Fetch total expenses after deleting an expense
                    fetchTotalExpenses();
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error('Error deleting expense:', error);
                }
            });
        }
    }
});
