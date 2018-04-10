

function login() {
  console.log("logging you in")
  var jsonData = getFormData($("#login-form"))
  console.log(jsonData)
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

$(document).ready(function() {
  $('#btn-login').click(function() {
      login();
  });
});

function getFormData($form){
  var unindexed_array = $form.serializeArray();
  var indexed_array = {};

  $.map(unindexed_array, function(n, i){
      indexed_array[n['name']] = n['value'];
  });

  return indexed_array;
}
