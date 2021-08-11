$(document).ready(function () {
  $("a.follow").click(function (e) {
    e.preventDefault();
    $.post(
      '{% url "user_follow" %}',
      {
        id: $(this).data("id"),
        action: $(this).data("action"),
      },
      function (data) {
        if (data["status"] == "ok") {
          var previous_action = $("a.follow").data("action");

          // toggle data-action
          $("a.follow").data(
            "action",
            previous_action == "follow" ? "unfollow" : "follow"
          );

          // toggle link text
          $("a.follow").text(
            previous_action == "follow" ? "Following" : "Follow"
          );

          // update total followers
          var previous_followers = parseInt($("span.count .total").text());

          $("span.count .total").text(
            previous_action == "follow"
              ? previous_followers + 1
              : previous_followers - 1
          );
        }
      }
    );
  });
});
