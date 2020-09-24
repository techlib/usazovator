function getColor(value) {
  //value from 0 to 1
  var hue = ((1 - value) * 120).toString(10);
  return ["hsl(", hue, ",100%,50%)"].join("");
}

function startRefresh() {
  up.reload('#page').then(() => {
    var max = 500;
    var current = parseInt($('#counter').text());
    $('#counter').css('color', getColor(current/max));
  })
}

$(function() {
  window.setInterval(startRefresh, 2000);
});

