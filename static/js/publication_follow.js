$(document).ready(function () {
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    
  $("a.pub__follow").click(function (e) {
    e.preventDefault();
    var pub_id = $(this).data('id');
    console.log(pub_id);

    $.post(
        $(this).data("url"),
      {
        csrfmiddlewaretoken: csrfToken,
        id: $(this).data("id"),
        action: $(this).data("action"),
      },
      function (data) {
        if (data["status"] == "ok") {
          var previous_action = $("a.pub__follow."+pub_id).data("action");

          // toggle data-action
          $("a.pub__follow."+pub_id).data("action", previous_action == "follow" ? "unfollow" : "follow");

          // toggle link text
          $("a.pub__follow."+pub_id).text(previous_action == "follow" ? "Following" : "Follow");

          // toggle class
          $('a.pub__follow.'+pub_id).toggleClass(previous_action == 'follow' || previous_action == 'unfollow' ? 'pub__following' : '');
          // update total pub__followers
          var previous_pub__followers = parseInt($("span.count .total").text());

          $("span#youand").text(previous_action == "follow" ? "You and" : "");
          $("span#more").text(previous_action == "follow" ? "more" : "");
        }
      }
    );
  });

  
});
