
$(document).ready(function() {

    
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    console.log("Document.ready");
    $("a.tag__follow").click(function (e) {
        e.preventDefault();
        var tag_id = $(this).data('id');
        console.log(tag_id);

        $.post(
            $(this).data("url"), {
                csrfmiddlewaretoken: csrfToken,
                id: $(this).data("id"),
                action: $(this).data("action"),
            },
            function (data) {
                if (data['status']=='ok') {
                    var previous_action = $('a.tag__follow.'+tag_id).data('action');

                    // toggle data-action
                    $('a.tag__follow.'+tag_id).data('action', previous_action == 'follow' ? 'unfollow' : 'follow');

                    // toggle link text
                    $('a.tag__follow.'+tag_id).html(previous_action == 'follow' ? '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="24" height="24" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M23 13.482L15.508 21L12 17.4l1.412-1.388l2.106 2.188l6.094-6.094L23 13.482zm-7.455 1.862L20 10.889V2H2v14c0 1.1.9 2 2 2h4.538l4.913-4.832l2.094 2.176zM8 13H4v-1h4v1zm3-2H4v-1h7v1zm0-2H4V8h7v1zm7-3H4V4h14v2z" fill="currentColor"/></svg>' : '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="24" height="24" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M23 16v2h-3v3h-2v-3h-3v-2h3v-3h2v3h3zM20 2v9h-4v3h-3v4H4c-1.1 0-2-.9-2-2V2h18zM8 13v-1H4v1h4zm3-3H4v1h7v-1zm0-2H4v1h7V8zm7-4H4v2h14V4z" fill="currentColor"/></svg>');

                    // toggle class
                    $('a.tag__follow.'+tag_id).toggleClass(previous_action == 'follow' || previous_action == 'unfollow' ? 'tag__following': '');
                }
            }
        )
    })

})
