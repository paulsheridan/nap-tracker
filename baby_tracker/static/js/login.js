

function login() {
  $.ajax({
    type: "POST",
    url: "/login",
    data: JSON.stringify({"email": "test@test.com", "password": "secret"}),
    dataType: "text",
    success: function(response){
      console.log('logged in')
    }
  });
}

$(document).ready(function() {
  login()
  // getLastMeal()
  // getLastNap()
  // $('#btn-refresh').click(function() {
  //     getDevices();
  // });
});
