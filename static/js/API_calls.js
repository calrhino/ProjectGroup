/**
 * Created by jarrett on 11/20/16.
 */
function create_class(name, desc) {
    $.post(create_class_url, {
            name: name,
            description: desc,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function join_class(class_id) {
    console.log(class_id);
    $.post(join_class_url, {
            class_id: class_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function leave_class(class_id) {
    $.post(leave_class_url, {
            class_id: class_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function create_project(class_id, name, desc) {
    $.post(create_project_url, {
            class_id: class_id,
            name: name,
            description: desc,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function join_project(project_id) {
    $.post(join_project_url, {
            project_id: project_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function leave_project(project_id) {
    $.post(leave_project_url, {
            project_id: project_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}


function create_group(project_id, name, desc) {
    $.post(create_group_url, {
            project_id: project_id,
            name: name,
            description: desc,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function join_group(group_id) {
    $.post(join_group_url, {
            group_id: group_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}

function leave_group(group_id) {
    $.post(leave_group_url, {
            group_id: group_id,
        }, function (msg) {
            console.log(msg);
        }
    );
}


function contact_member(member, msg) {
    $.post(contact_user_url,
        {
            id: member.id,
            msg: msg
        }, function (msg) {
            console.log(msg);
        });
}