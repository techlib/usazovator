function startRefresh() {
  $.get(document.location, function(data) {
    $(document.body).html(data);
  });
}

$(function() {
  setTimeout(startRefresh, 5000);
});
