/**
 * Created by jarrett on 11/20/16.
 */
function add_student(auth_id) {
    $.post(add_student_url, {
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}
function create_class(auth_id, name, desc) {
    $.post(create_class_url, {
            name: name,
            description: desc,
            auth_id: auth_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function join_class(auth_id, class_id) {
    $.post(join_class_url, {
            class_id: class_id,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}

function leave_class(auth_id, class_id) {
    $.post(leave_class_url, {
            class_id: class_id,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}

function create_project(auth_id, class_id, name, desc) {
    $.post(create_project_url, {
            class_id: class_id,
            name: name,
            description: desc,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}

function join_project(auth_id, project_id) {
    $.post(join_project_url, {
            project_id: project_id,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}

function leave_project(auth_id, project_id) {
    $.post(leave_project_url, {
            project_id: project_id,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}


function create_group(auth_id, project_id, name, desc) {
    $.post(create_group_url, {
            project_id: project_id,
            name: name,
            description: desc,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}

function join_group(auth_id, group_id) {
    $.post(join_group_url, {
            group_id: group_id,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}

function leave_group(auth_id, group_id) {
    $.post(leave_group_url, {
            group_id: group_id,
            auth_id: auth_id
        }, function (msg) {
            console.log(msg);
        }
    );
}


