function upTime(countFrom) {
  now = new Date();
  countFrom = new Date(countFrom);
  difference = (now-countFrom);

  days=Math.floor(difference/(60*60*1000*24)*1);
  hours=Math.floor((difference%(60*60*1000*24))/(60*60*1000)*1);
  mins=Math.floor(((difference%(60*60*1000*24))%(60*60*1000))/(60*1000)*1);
  secs=Math.floor((((difference%(60*60*1000*24))%(60*60*1000))%(60*1000))/1000*1);

  document.getElementById('days').firstChild.nodeValue = days;
  document.getElementById('hours').firstChild.nodeValue = hours;
  document.getElementById('minutes').firstChild.nodeValue = mins;
  document.getElementById('seconds').firstChild.nodeValue = secs;

  clearTimeout(upTime.to);
  upTime.to=setTimeout(function(){ upTime(countFrom); },1000);
}

function getLastNap() {
  $.ajax({
    type: "GET",
    url: "/nap/current",
    success: function(response){
      console.log(response)
      upTime(moment().format(response.start))
    }
  });
}

function startNap() {
  $.ajax({
    type: "POST",
    url: "/nap/start",
    success: function(){
      getLastNap()
    }
  });
}

$(document).ready(function() {
  console.log('hello')
  getLastNap()
  $('#btn-timer-start').click(function() {
      startNap();
  });
});
