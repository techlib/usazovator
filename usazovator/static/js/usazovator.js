function getColor(value) {
  //value from 0 to 1
  var hue = ((1 - value) * 120).toString(10);
  return ["hsl(", hue, ",100%,50%)"].join("");
}

function startRefresh() {
  up.reload('html').then(() => {
    var max = 500;
    var current = parseInt($('#counter').text());
    $('#counter').css('color', getColor(current/max));
    setTimeout(startRefresh, 1000);
  })
}

$(function() {
  setTimeout(startRefresh, 1000);
});

