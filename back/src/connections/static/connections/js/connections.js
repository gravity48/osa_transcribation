function show_connect(msg) {
    $('#show_connections').click();
}

function show_tasks(msg){
    $('#show_tasks').click();
}

function del_commit_con(msg) {
    $('#Modal').modal('hide');
    $('#show_connections').click();
}

function del_commit_task(msg){
    $('#Modal').modal('hide');
    $('#show_tasks').click();
}

function del_by_id(event) {
    let data = event.data;
    if (data['event'] === 'del_connection'){
        send_json_ajax(data, data['url'], del_commit_con, console_log);
    }
    if(data['event'] === 'del_task') {
        send_json_ajax(data, data['url'], del_commit_task, console_log);
    }
}

$(document).ready(function () {
    $(document).on('click', '#add-connect-btn', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let data_url = $(this).attr("data-url");
        clear_form('.add-connection-block form');
        let [data, status] = json_from_form('.add-connection-block form');
        let target = $(this).attr('data-target');
        if (status) {
            if (target === 'connection') {
                send_json_ajax(data, data_url, show_connect, show_exception_on_form, '.add-connection-block form');
            }
            if(target === 'task'){
                send_json_ajax(data, data_url, show_tasks, show_exception_on_form, '.add-connection-block form');
            }
        }
    });
    $(document).on('click', 'tr .buttons > #del-button', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let alias = $(this).attr("data-alias");
        let params = {
            'url': $(this).attr("data-url"),
        };
        let target = $(this).attr("data-target");
        if (target === 'connection'){
            params['con_id'] = $(this).attr("data-con_id");
            params['event'] = 'del_connection';
        }
        if (target === 'task'){
            params['task_id'] = $(this).attr("data-task_id");
            params['event'] = 'del_task';
        }
        show_popup_form('#Modal', 'Удалить запись ' + alias + '?', 'COMMIT', del_by_id, params);
    });
});