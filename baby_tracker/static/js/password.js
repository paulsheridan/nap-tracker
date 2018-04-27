$(document).ready(function() {
  var secret = extractSecret();
});

function hideMsg() {
  $(".msg-green").hide();
  $(".msg-red").hide();
}

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
    statusCode: {
      200: function() {
        hideMsg();
        $("#reset-success").show();
        $(".form-control").val("");
      },
      // Bad Request error handling displays a 'password too short or contains spaces' error
      400: function() {
        hideMsg();
        $("#bad-password").show();
        $(".form-control").val("");
      },
      // Unauthorized error handling displays a 'reset secret not valid, please request another' error
      401: function() {
        hideMsg();
        $("#bad-code").show();
        $(".form-control").val("");
      },
    }
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
      hideMsg();
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
