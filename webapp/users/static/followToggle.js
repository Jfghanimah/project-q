$(document).ready(function() {
  // Use event delegation to handle clicks on buttons added dynamically
  $(document).on('click', '.follow-toggle', function(e) {
    e.preventDefault();
    var $btn = $(this);
    var actionUrl = $btn.data('action-url');
    var currentState = $btn.data('state');
    var method = (currentState === 'following') ? 'DELETE' : 'POST';

    $.ajax({
      url: actionUrl,
      type: method, // Use POST to follow, DELETE to unfollow
      success: function(response) {
        // Update follower count if the element exists
        var $followerCount = $('.follower-count-number');
        if ($followerCount.length && response.follower_count !== undefined) {
          $followerCount.text(response.follower_count);
        }

        // Toggle button state
        if (method === 'DELETE') {
          // Switched from following to not_following
          $btn.data('state', 'not_following');
          $btn.removeClass('btn-following btn-danger').addClass('btn-follow').text("Follow");
        } else {
          // Switched from not_following to following
          $btn.data('state', 'following');
          $btn.removeClass('btn-follow').addClass('btn-following').text("Following");
        }
      },
      error: function(xhr) {
        const error = xhr.responseJSON?.detail?.error || "An unknown error occurred.";
        alert("Error: " + error);
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
