$(document).ready(function() {
  // Bind click event on all buttons with class 'follow-toggle'
  $('.follow-toggle').click(function(e) {
    e.preventDefault();
    var $btn = $(this);
    var actionUrl = $btn.data('action-url');
    $.ajax({
      url: actionUrl,
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').first().val()
      },
      success: function(response) {
        //alert(response.message);
        // Toggle button state based on current state:
        if ($btn.data('state') === 'following') {
          // Switch from following to not following:
          $btn.data('state', 'not_following');
          $btn.removeClass('btn-following btn-danger').addClass('btn-follow');
          $btn.text("Follow");
          $btn.data('action-url', $btn.data('follow-url'));
        } else {
          // Switch from not following to following:
          $btn.data('state', 'following');
          $btn.removeClass('btn-follow').addClass('btn-following');
          $btn.text("Following");
          $btn.data('action-url', $btn.data('unfollow-url'));
        }
      },
      error: function(xhr) {
        alert("Error: " + (xhr.responseJSON.error || "Unknown error"));
      }
    });
  });

  // Hover behavior for buttons in 'following' state
  $('.follow-toggle').hover(
    function() {
      var $btn = $(this);
      if ($btn.data('state') === 'following') {
        $btn.text("Unfollow");
        $btn.removeClass('btn-following').addClass('btn-danger');
      }
    },
    function() {
      var $btn = $(this);
      if ($btn.data('state') === 'following') {
        $btn.text("Following");
        $btn.removeClass('btn-danger').addClass('btn-following');
      }
    }
  );
});

// CSRF setup remains unchanged
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = $.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});
