function getColor(value) {
    hue0 = 120
    hue1 = 0
    var hue = (value * (hue1 - hue0)) + hue0;
    return 'hsl(' + hue + ', 100%, 50%)';
}

function startRefresh() {
  up.reload('#page').then(() => {
    var max = 1200;
    var current = parseInt($('#counter').text());
    $('#counter').css('color', getColor(current/max));
  })
}

$(function() {
  window.setInterval(startRefresh, 2000);
});

