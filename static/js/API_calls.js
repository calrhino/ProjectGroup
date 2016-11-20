/**
 * Created by jarrett on 11/20/16.
 */
var auth_id = 12345;
function add_student() {
    $.post(add_student_url, {
            auth_id:auth_id
        }, function(msg) {
            console.log(msg);
        }
    );
}
function create_class(name, desc) {
    $.post(create_class_url, {
            name:name,
            description:desc,
            auth_id:auth_id,
        }, function(msg) {
            console.log(msg);
        }
    );
}

function join_class(class_id) {
    $.post(join_class_url, {
            class_id:class_id,
            auth_id:auth_id
        }, function(msg) {
            console.log(msg);
        }
    );
}

function leave_class(class_id) {
    $.post(leave_class_url, {
            class_id:class_id,
            auth_id:auth_id
        }, function(msg) {
            console.log(msg);
        }
    );
}

function create_project(class_id, name, desc) {
    $.post(create_project_url, {
            class_id:class_id,
            name:name,
            description:desc,
            auth_id:auth_id
        }, function(msg) {
            console.log(msg);
        }
    );
}

function join_project(project_id) {
    $.post(join_project_url, {
            project_id:project_id,
            auth_id:auth_id
        }, function(msg) {
            console.log(msg);
        }
    );
}

function leave_project(project_id) {
    $.post(leave_project_url, {
            project_id:project_id,
            auth_id:auth_id
        }, function(msg) {
            console.log(msg);
        }
    );
}


