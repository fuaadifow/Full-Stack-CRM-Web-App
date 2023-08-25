$(document).ready(function() {
  $('.btn-delete-task').on('click', function() {
    const taskId = $(this).data('id');
    const deleteUrl = deleteUrls.replace('0', taskId);
    const $confirmDeleteModal = $('#confirmDeleteModal');
    $confirmDeleteModal.find('.btn-confirm-delete').attr('href', deleteUrl);
    $confirmDeleteModal.modal('show');
  });

  // Confirm delete
  $('#confirmDeleteModal').on('show.bs.modal', function(event) {
    const deleteUrl = $(event.relatedTarget).attr('href');
    $(this).find('.btn-confirm-delete').attr('href', deleteUrl);
  });

  // Search function
  $('#searchInput').on('keyup', function() {
    const value = $(this).val().toLowerCase();
    $('#taskTable tbody tr').filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});


