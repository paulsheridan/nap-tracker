var timedifference = new Date().getTimezoneOffset();
window.onload=function() {
  // Month,Day,Year,Hour,Minute,Second
  // upTime('jan,01,2014,00:00:00'); // ****** Change this line!
}
function upTime(countTo) {
  now = new Date();
  countTo = new Date(countTo);
  difference = (now-countTo);

  days=Math.floor(difference/(60*60*1000*24)*1);
  hours=Math.floor((difference%(60*60*1000*24))/(60*60*1000)*1);
  mins=Math.floor(((difference%(60*60*1000*24))%(60*60*1000))/(60*1000)*1);
  secs=Math.floor((((difference%(60*60*1000*24))%(60*60*1000))%(60*1000))/1000*1);

  document.getElementById('days').firstChild.nodeValue = days;
  document.getElementById('hours').firstChild.nodeValue = hours;
  document.getElementById('minutes').firstChild.nodeValue = mins;
  document.getElementById('seconds').firstChild.nodeValue = secs;

  clearTimeout(upTime.to);
  upTime.to=setTimeout(function(){ upTime(countTo); },1000);
}

function getLastNap() {
  $.ajax({
    type: "GET",
    url: "/today/naps",
    success: function(response){
      for(var i = 0; i < response.length; i++) {
        var obj = response[i];
        console.log(obj.id);
      }
    }
  });
}

function getLastMeal() {
  $.ajax({
    type: "GET",
    url: "/today/meals",
    success: function(response){
      for(var i = 0; i < response.length; i++) {
        var obj = response[i];
        console.log(obj.id);
      }
    }
  });
}

$(document).ready(function() {
  console.log('hello')
  getLastMeal()
  getLastNap()
  // $('#btn-refresh').click(function() {
  //     getDevices();
  // });
});
