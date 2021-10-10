$(document).ready(function () {
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
    
    console.log("Works");

    $("button#yes_leave").click(function (e) {
        e.preventDefault();
        var pub_id = $(this).data('id');

        $.post(
            $(this).data("url"), {
                csrfmiddlewaretoken: csrfToken,
                id: $(this).data("id"),
            },
            function (data) {
                if (data["status"] == 'ok') {
                    console.log("I will remove that publication");
                    $("#"+pub_id).remove();
                }
                if (data["status"] == 'error') {
                    console.log("Error");
                }
            }
        )
    })
});