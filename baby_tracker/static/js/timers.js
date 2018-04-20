function upTime(countFrom) {
  now = new Date();
  countFrom = new Date(countFrom);
  difference = (now-countFrom);
  timeArr = formatTime(difference)

  document.getElementById('days').firstChild.nodeValue = timeArr[0];
  document.getElementById('hours').firstChild.nodeValue = timeArr[1];
  document.getElementById('minutes').firstChild.nodeValue = timeArr[2];
  document.getElementById('seconds').firstChild.nodeValue = timeArr[3];

  clearTimeout(upTime.to);
  upTime.to=setTimeout(function(){upTime(countFrom);},1000);
}

function formatTime(difference) {
  days = Math.floor(difference/(60*60*1000*24)*1);
  hours = Math.floor((difference%(60*60*1000*24))/(60*60*1000)*1);
  mins = Math.floor(((difference%(60*60*1000*24))%(60*60*1000))/(60*1000)*1);
  secs = Math.floor((((difference%(60*60*1000*24))%(60*60*1000))%(60*1000))/1000*1);
  return [days, hours, mins, secs]
}

function getLastNap() {
  $.ajax({
    type: "GET",
    url: "/nap/current",
    success: function(response){
      if (response.end) {
        listLastNap(response)
        $('.timer-start').show();
        $('.timer-end').hide();
      } else {
        upTime(moment().format(response.start));
        $('.timer-start').hide();
        $('.timer-end').show();
      }
    }
  });
}

function listLastNap(response) {
  $('#previous-timer').empty();
  timeArr = formatTime(new Date(response.end) - new Date(response.start))
  for (var i = 0; i < timeArr.length; i++) {
    li = $('<li/>')
    li.text(timeArr[i])
    li.addClass('previous-naps')
    $('#previous-timer').append(li);

  }
}

function startNap() {
  $.ajax({
    type: "POST",
    url: "/nap/start",
    success: function(){
      getLastNap();
    }
  });
}

function endNap() {
  $.ajax({
    type: "PUT",
    url: "/nap/end",
    success: function(){
      getLastNap();
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
