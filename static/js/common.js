document.addEventListener("DOMContentLoaded", () => {
  const loadingDialog = document.getElementById("loading-dialog");

  // Show loading dialog
  function showLoading() {
    loadingDialog.classList.remove("hidden");
  }

  // Hide loading dialog
  function hideLoading() {
    loadingDialog.classList.add("hidden");
  }

  // Export functions if needed globally
  window.showLoading = showLoading;
  window.hideLoading = hideLoading;
});