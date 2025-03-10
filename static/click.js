// document.ready function
$(document).ready(function () {
    $('#watchLiveSwitch_1').click(function (e) {
        e.preventDefault(); // prevent form from reloading page
        let check = $(".");
        $.ajax({
            'url': '/capture_video',
            'type': 'POST',
            'data': {'state':check},
             error: function () {alert('Error')},
            'success': function (data) {
                if (data == "success") {
                    alert('request sent!');
                }
            }
        });
    });
});