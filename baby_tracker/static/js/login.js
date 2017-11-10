

function login() {
  $.ajax({
    type: "POST",
    url: "/login",
    data: JSON.stringify({"email": "new@guy.com", "password": "new"}),
    dataType: "text",
    success: function(response){
      console.log('logged in')
    }
  });
}

$(document).ready(function() {
  console.log('hello')
  login()
  getLastMeal()
  getLastNap()
  // $('#btn-refresh').click(function() {
  //     getDevices();
  // });
});
