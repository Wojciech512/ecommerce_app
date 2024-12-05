function showModal() {
  const modal = document.getElementById('operationModal');
  modal.classList.remove('fade-out');
  modal.classList.add('show', 'fade-in');
}

function closeModal() {
  const modal = document.getElementById("operationModal");
  modal.classList.remove('fade-in');
  modal.classList.add('fade-out');

  modal.addEventListener('animationend', function handleClose() {
    modal.classList.remove('show');
    modal.removeEventListener('animationend', handleClose);
  }, { once: true });
}

function openEditProductModal(button) {
  const productId = button.getAttribute('data-productid');
  window.location.href = '/account/admin/update-product/' + productId + '/';
}

function confirmDeleteProduct(button) {
  const productId = button.getAttribute('data-productid');
  document.getElementById('modalMessage').innerHTML =  button.getAttribute("data-message");
  document.getElementById('operationForm').action = '/account/admin/delete-product/' + productId + '/';
  document.getElementById('operationType').value = 'delete_product';
  document.getElementById('productId').value = productId;
  showModal();
}

function confirmDeleteUser(button) {
  const userId = button.getAttribute("data-userid");
  document.getElementById('modalMessage').innerHTML = button.getAttribute("data-message");
  document.getElementById('operationForm').action = '/account/admin/delete-user/' + userId + '/';
  document.getElementById('operationType').value = 'delete_user';
  document.getElementById('userId').value = userId;
  showModal();
}

function confirmChangePermissions(button) {
  const userId = button.getAttribute("data-userid");
  document.getElementById('modalMessage').innerHTML = button.getAttribute("data-message");
  document.getElementById('operationForm').action = '/account/admin/change-user-permissions/' + userId + '/';
  document.getElementById('operationType').value = 'change_permissions';
  document.getElementById('userId').value = userId;
  showModal();
}

function confirmDeleteLogs(button) {
  document.getElementById('modalMessage').innerHTML = button.getAttribute("data-message");
  document.getElementById('operationForm').action = '/account/admin/delete-logs/';
  document.getElementById('operationType').value = 'delete_logs';
  showModal();
}

function openModal(button) {
  const operationType = button.getAttribute("data-operation");
  document.getElementById("operationType").value = operationType;

  if (operationType === 'delete_product') {
    confirmDeleteProduct(button);
  } else if (operationType === 'delete_user') {
    confirmDeleteUser(button);
  } else if (operationType === 'change_permissions') {
    confirmChangePermissions(button);
  } else if (operationType === 'delete_logs') {
    confirmDeleteLogs(button);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const deleteUserButtons = document.querySelectorAll('.delete-user-button');
  deleteUserButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      openModal(this);
    });
  });

  const changePermissionButtons = document.querySelectorAll('.set-admin-user-button, .set-user-admin-button');
  changePermissionButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      openModal(this);
    });
  });

  const editProductButtons = document.querySelectorAll('.edit-product-button');
  editProductButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      openEditProductModal(this);
    });
  });

  const deleteProductButtons = document.querySelectorAll('.delete-product-button');
  deleteProductButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      openModal(this);
    });
  });

  const deleteLogsButtons = document.querySelectorAll('.delete-logs-button');
  deleteLogsButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      openModal(this);
    });
  });
});
