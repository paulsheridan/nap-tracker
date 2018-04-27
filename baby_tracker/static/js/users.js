function login() {
  var jsonData = getFormData($("#login-form"))
  $.ajax({
    type: "POST",
    url: "/login",
    data: JSON.stringify(jsonData),
    dataType: "text",
    success: function(response){
      location.href = "/timers"
    },
    error: function(response){
      $("#wrong-pass").show()
    }
  });
}

function logout() {
  $.ajax({
    type: "POST",
    url: "/logout",
    success: function(response){
      location.href = "/"
    }
  });
}

function signup() {
  var jsonData = getFormData($("#signup-form"))
  $.ajax({
    type: "POST",
    url: "/users",
    data: JSON.stringify(jsonData),
    dataType: "text",
    statusCode: {
      400: function() {
        $("#email-exist").show();
      }
    },
    success: function(response){
      location.href = "/"
    }
  });
}

function getFormData($form){
  var unindexedArray = $form.serializeArray();
  var indexedArray = {};
  $.map(unindexedArray, function(n, i){
      indexedArray[n['name']] = n['value'];
  });
  return indexedArray;
}

$(document).ready(function() {
  $("#login-form").submit(function(e) {
    e.preventDefault();
    login();
  });
  $('#btn-logout').click(function() {
      logout();
  });
  $("#signup-form").submit(function(e) {
    e.preventDefault();
    signup();
  });

  if (document.cookie.indexOf('auth_tkt') == -1 ) {
    $(".nav-login").show()
  }
  else {
    $(".nav-user").show()
  }
});
