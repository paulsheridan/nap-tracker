$(document).ready(function() {
  var secret = extractSecret();
});

function extractSecret() {
  secret = window.location.href.toString().split("/").pop()
  return secret
}

function resetPassword(secret) {
  var jsonData = getFormData($("#reset-form"))
  jsonData.reset_secret = secret
  $.ajax({
    type: "POST",
    url: "/reset/password",
    data: JSON.stringify(jsonData),
    dataType: "text",
    success: function(response) {
      $("#reset-success").show();
      $(".form-control").val("");
    },
  });
}

function requestResetEmail() {
  var jsonData = getFormData($("#reset-email-request"))
  $.ajax({
    type: "POST",
    url: "/reset/secretlink",
    data: JSON.stringify(jsonData),
    dataType: "text",
    complete: function(response) {
      $("#link-success").show();
      $(".form-control").val("");
    },
  });
}

$("#reset-form").submit(function(e) {
  e.preventDefault();
  resetPassword(secret)
});

$("#reset-email-request").submit(function(e) {
  e.preventDefault();
  requestResetEmail()
});
