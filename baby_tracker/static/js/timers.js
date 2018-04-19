function upTime(countFrom) {
  now = new Date();
  countFrom = new Date(countFrom);
  difference = (now-countFrom);

  days = Math.floor(difference/(60*60*1000*24)*1);
  hours = Math.floor((difference%(60*60*1000*24))/(60*60*1000)*1);
  mins = Math.floor(((difference%(60*60*1000*24))%(60*60*1000))/(60*1000)*1);
  secs = Math.floor((((difference%(60*60*1000*24))%(60*60*1000))%(60*1000))/1000*1);

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
      if (response.end) {
        $('#previous-timer').empty()
        $('#previous-timer').append(document.createTextNode(response.start));
        $('#previous-timer').append(document.createTextNode(response.end));
        $('.timer-start').show()
        $('.timer-end').hide()
      } else {
        upTime(moment().format(response.start))
        $('.timer-start').hide()
        $('.timer-end').show()
      }
    }
  });
}

function printNap(start, end) {
  $('#previous-timer').appendChild(document.createTextNode("Water"));
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

function endNap() {
  $.ajax({
    type: "PUT",
    url: "/nap/end",
    success: function(){
      getLastNap()
    }
  });
}

$(document).ready(function() {
  getLastNap()
  $('.timer-start').click(function() {
      startNap();
  });
  $('.timer-end').click(function() {
      endNap();
  });
});
