function login() {
  var jsonData = getFormData($("#login-form"))
  $.ajax({
    type: "POST",
    url: "/login",
    data: JSON.stringify(jsonData),
    dataType: "text",
    success: function(response){
      location.href = "timers"
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

function getFormData($form){
  var unindexed_array = $form.serializeArray();
  var indexed_array = {};
  $.map(unindexed_array, function(n, i){
      indexed_array[n['name']] = n['value'];
  });
  return indexed_array;
}

$(document).ready(function() {
  $('#btn-login').click(function() {
      login();
  });
  $('#btn-logout').click(function() {
      logout();
  });
});
