function show_content(msg){
    $('#content-block').html(msg.render_content);
}

function event_list(){
    $(document).on('click', '#logout-href', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let data_url = $(this).attr("data-url");
        let data = {'event': 'logout'}
        send_json_ajax(data, data_url, reload_window, console_log);
    });
    $(document).on('click', '#show_connections', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let data = {'event': 'show_connections'};
        send_json_ajax(data, '', show_content, console_log);
    });
    $(document).on('click', '#show_tasks', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let data = {'event': 'show_tasks'};
        send_json_ajax(data, '', show_content, console_log);
    });
}

$(document).ready(event_list);