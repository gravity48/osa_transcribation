function win_reload(msg){
    $('#Modal').modal('hide');
    $('#show_tasks').click();
}

function manage_event(event){
    let params = event.data
    send_json_ajax(params, params['url'], win_reload, console_log);
}

$(document).ready(function () {
    $(document).on('click', 'tr .buttons > .management-btn', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let alias = $(this).attr("data-alias");
        let params = {
            'url': $(this).attr("data-url"),
            'event': $(this).attr("data-event"),
            'task_id': $(this).attr("data-task_id"),
        };
        let text = ""
        if (params['event'] === 'play'){
            text = 'Запустить задачу ' + alias + '?';
        }
        if (params['event'] === 'stop'){
            text = 'Остановить задачу ' + alias + '?';
        }
        show_popup_form('#Modal', text, 'COMMIT', manage_event, params);
    });
});