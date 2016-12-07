/**
 * Created by jarrett on 11/12/16.
 */

function extend(a, b) {
    for (var i = 0; i < b.length; i++) {
        a.push(b[i]);
    }
}

var main_content = new Vue({
        el: "#main_content",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            page: 'welcome',
            bg_idx: 0,
            background: 'bg0',
            sel_class: -1,
            sel_project: -1,
            sel_group: -1,
            sel_member: -1,
            class_name:'',
            user_message: '',
            is_contact: false,
            is_edit_status: false,
            allclasses: [],
            messages: [],
            classes: [],
            create: {
                new_class: {
                    name: '',
                    description: '',
                    edit: false,
                },
                new_project: {
                    name: '',
                    description: '',
                    edit: false,
                },
                new_group: {
                    name: '',
                    description: '',
                    edit: false,
                }
            }

        },
        methods: {
            // Get : classes, projects, groups, members, messages
            // Replaces current data with newly retrieved data
            // These should be getJSON() for resources sake
            getClasses: function () {
                $.post(get_classes_url,
                    {}, function (data) {
                        //console.log(data)
                        main_content.classes = [];
                        extend(main_content.classes, data.classes);
                    }
                );
            },
            getProjects: function () {
                var class_el = this.classes[this.sel_class];
                $.post(get_projects_url,
                    {
                        class_id: class_el.id
                    }, function (data) {
                        //console.log(data);
                        if (data.projects[0] != null)
                            extend(class_el.projects, data.projects);
                    }
                )
            },
            getGroups: function () {
                var project = this.classes[this.sel_class].projects[this.sel_project];
                $.post(get_groups_url,
                    {
                        project_id: project.id,
                    }, function (data) {
                        //console.log(data);
                        if (data.groups[0] != null)
                            extend(project.groups, data.groups);
                    }
                );
            },
            getMembers: function (proj_idx, group_idx) {
                var group = this.classes[this.sel_class].projects[this.sel_project].groups[this.sel_group];
                $.post(get_members_url,
                    {
                        group_id: group.id
                    }, function (data) {
                        //console.log(data);
                        if (data.members[0] != null)
                            extend(group.members, data.members);
                    }
                );
            },

            getAllClasses: function () {
                $.post(get_all_classes_url,
                    {}, function (data) {
                        main_content.allclasses = [];
                        extend(main_content.allclasses, data.classes);
                    }
                );
            },
            getMessages: function () {
                $.post(get_messages_url,
                    {}, function (data) {
                        main_content.messages = {sent: [], received: []};
                        if (data.sent_messages[0] != null)
                            extend(main_content.messages.sent, data.sent_messages);
                        if (data.received_messages[0] != null)
                            extend(main_content.messages.received, data.received_messages);
                    }
                );
            },

            // Create : class, project, group -----------------------------------------------------
            createClass: function () {
                this.create.new_class.edit = false;
                var obj = this.create.new_class;
                $.post(create_class_url, {
                        name: obj.name,
                        description: obj.description,
                    }, function (data) {
                        //console.log(data);
                        main_content.classes.push(data)
                    }
                );
                this.hideCreateClass();
            },
            createProject: function () {
                this.create.new_project.edit = false;
                var obj = this.create.new_project;
                var id = this.classes[this.sel_class].id;
                $.post(create_project_url, {
                        class_id: id,
                        name: obj.name,
                        description: obj.description,
                    }, function (data) {
                        //console.log(data);
                        main_content.classes[main_content.sel_class].projects.push(data);
                    }
                );
                this.hideCreateProject();
            },
            createGroup: function () {
                this.create.new_group.edit = false;
                var obj = this.create.new_group;
                var id = this.classes[this.sel_class].projects[this.sel_project].id;
                $.post(create_group_url, {
                        project_id: id,
                        name: obj.name,
                        description: obj.description,
                    }, function (data) {
                        //console.log(data);
                        main_content.classes[main_content.sel_class].projects[main_content.sel_project].groups.push(data);
                    }
                );
                this.hideCreateGroup();
            },

            // set and update "page" of the single-page view --------------------------------------
            setPage: function (page) {
                if (this.page == page) return;
                this.page = page;
                if (page == 'loggedin' && this.classes.length == 0)
                    this.getClasses();
                else if (page == 'joinclass' && this.allclasses.length == 0)
                    this.getAllClasses();
                else if (page == 'mymessages' && this.messages.length == 0)
                    this.getMessages();
            },
            updatePage: function (page) {
                if (page == 'loggedin') {
                    this.hideClass();
                    this.getClasses();
                }
                else if (page == 'joinclass') {
                    this.getAllClasses();
                }
                else if (page == 'mymessages') {
                    this.getMessages();
                }
            },

            // Toggle Functions to Control Visuals ------------------------------------------------
            toggleClass: function (class_idx) {
                if (this.sel_class == class_idx)
                    this.hideClass();
                else {
                    this.sel_class = class_idx;
                    this.class_name=this.classes[this.sel_class].name;
                    if (this.classes[class_idx].projects[0] == null) {
                        this.getProjects();
                    }
                }
            },
            toggleProject: function (proj_idx) {
                if (this.sel_project == proj_idx)
                    this.hideProject();
                else {
                    this.sel_project = proj_idx;
                    if (this.classes[this.sel_class].projects[proj_idx].groups[0] == null) {
                        this.getGroups();
                    }
                }
            },
            toggleGroup: function (group_idx) {
                if (this.sel_group == group_idx) {
                    this.hideGroup();
                }
                else {
                    this.sel_group = group_idx;
                    if (this.classes[this.sel_class].projects[this.sel_project].groups[group_idx].members[0] == null) {
                        this.getMembers();
                    }
                }
            },
            toggleMember: function (idx) {
                if (this.sel_member == idx)
                    this.showAllMember()
                else
                    this.sel_member = idx;
            },
            toggleEditStatus: function () {
                this.is_edit_status = !this.is_edit_status;
            },
            toggleCreateClass: function () {
                this.create.new_class.edit = !this.create.new_class.edit;
            },
            toggleCreateProject: function () {
                this.create.new_project.edit = !this.create.new_project.edit;
            },
            toggleCreateGroup: function () {
                this.create.new_group.edit = !this.create.new_group.edit;
            },
            showContact: function () {
                this.is_contact = true;
            },
            hideClass: function () {
                this.sel_class = -1;
                this.class_name = '';
                this.hideProject();
            },
            hideProject: function () {
                this.hideGroup();
                this.sel_project = -1;
            },
            hideGroup: function () {
                this.showAllMember();
                this.hideContact();
                this.hideEditStatus();
                this.sel_group = -1;
            },
            showAllMember: function () {
                this.sel_member = -1;
            },
            hideContact: function () {
                this.is_contact = false;
                this.clearMessage();
            },
            hideEditStatus: function () {
                this.is_edit_status = false;
            },
            clearMessage: function () {
                this.user_message = '';
            },
            hideCreateClass: function () {
                this.create.new_class.name = '';
                this.create.new_class.description = '';
                this.create.new_class.edit = false;
            },
            hideCreateProject: function () {
                this.create.new_project.name = '';
                this.create.new_project.description = '';
                this.create.new_project.edit = false;
            },
            hideCreateGroup: function () {
                this.create.new_group.name = '';
                this.create.new_group.description = '';
                this.create.new_group.edit = false;
            },

            // message related calls --------------------------------------------------------------
            setGroupStatus: function () {
                var group = this.classes[this.sel_class].projects[this.sel_project].groups[this.sel_group];
                group._pending = true;
                $.post(set_group_status_url,
                    {
                        group_id: group.id,
                        new_status: group.new_status
                    }, function (data) {
                        //console.log(data);
                        group.status = group.new_status;
                        main_content.hideEditStatus();
                        group._pending = false;
                    })
            },

            contact_member: function (member, msg) {
                $.post(contact_user_url,
                    {
                        id: member.id,
                        msg: msg
                    }, function (data) {
                        main_content.messages.sent.unshift(data.message);
                        //console.log(msg);
                    }
                );
            },
            contactMembers: function () {
                var message = this.user_message;
                this.hideContact();
                var members = this.classes[this.sel_class].projects[this.sel_project].groups[this.sel_group].members;
                if (this.sel_member < 0) {
                    for (var i = 0, len = members.length; i < len; i++) {
                        this.contact_member(members[i], message)
                    }
                } else {
                    this.contact_member(members[this.sel_member], message);
                }
            },

            request_join_group_member: function (member_id, message) {
                $.post(request_join_group_url, {
                        id: member_id,
                        group_id: this.classes[this.sel_class].projects[this.sel_project].groups[this.sel_group].id,
                        msg: message
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
            },
            request_join_group: function () {
                var message = this.user_message;
                this.hideContact();
                var members = this.classes[this.sel_class].projects[this.sel_project].groups[this.sel_group].members;
                if (this.sel_member < 0) {
                    for (var i = 0, len = members.length; i < len; i++) {
                        this.request_join_group_member(members[i].id, message)
                    }
                } else {
                    this.request_join_group_member(members[this.sel_member].id, message);
                }
            },
            accept_join_group: function (id) {
                $.post(accept_join_group_url, {
                        id: id
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
            },
            reject_join_group: function (id) {
                $.post(reject_join_group_url, {
                        id: id
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
            },

            delete_message: function (id, idx, is_sender) {
                $.post(delete_message_url, {
                        id: id,
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
                if (is_sender)
                    this.messages.sent.splice(idx, 1);
                else
                    this.messages.received.splice(idx, 1);

            },

            // Join, Leave Delete : classes, projects, groups -------------------------------------
            join_class: function (class_idx) {
                $.post(join_class_url, {
                        class_id: this.allclasses[class_idx].id,
                    }, function (data) {
                        //console.log(data);
                        main_content.classes.push(data);
                    }
                );
                this.allclasses.splice(class_idx, 1);
            },
            leave_class: function () {
                var sel_class = this.sel_class;
                $.post(leave_class_url, {
                        class_id: this.classes[sel_class].id,
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
                this.classes.splice(sel_class, 1);
                this.hideClass();
            },
            delete_class: function () {
                var sel_class = this.sel_class;
                this.hideClass();
                $.post(delete_class_url, {
                        class_id: this.classes[sel_class].id,
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
                this.classes.splice(sel_class, 1);
            },

            delete_project: function () {
                var sel_class = this.sel_class, sel_project = this.sel_project;
                this.hideProject();
                this.classes[sel_class].projects.splice(sel_project, 1);
                $.post(delete_project_url, {
                        project_id: this.classes[sel_class].projects[sel_project].id,
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
            },

            join_group: function () {
                var sel_class = this.sel_class, sel_project = this.sel_project, sel_group = this.sel_group;
                this.classes[sel_class].projects[sel_project].groups[sel_group].is_group = true;
                $.post(join_group_url, {
                        group_id: this.classes[sel_class].projects[sel_project].groups[sel_group].id,
                    }, function (data) {
                        data.is_user = true;
                        //console.log(data);
                        main_content.classes[sel_class].projects[sel_project].groups[sel_group].members.push(data);
                    }
                );
            },
            leave_group: function () {
                var sel_class = this.sel_class, sel_project = this.sel_project, sel_group = this.sel_group;
                this.classes[sel_class].projects[sel_project].groups[sel_group].is_group = false;
                $.post(leave_group_url, {
                        group_id: this.classes[sel_class].projects[sel_project].groups[sel_group].id,
                    }, function (msg) {
                        //console.log(msg);
                        var group = main_content.classes[sel_class].projects[sel_class].groups[sel_class];
                        for (var i = 0, len = group.members.length; i < len; i++)
                            if (group.members[i].is_user == true)
                                group.members.splice(i, 1);
                    }
                );
            },
            delete_group: function () {
                var sel_class = this.sel_class, sel_project = this.sel_project, sel_group = this.sel_group;
                this.hideGroup();
                $.post(delete_group_url, {
                        group_id: this.classes[sel_class].projects[sel_project].groups[sel_group].id,
                    }, function (msg) {
                        //console.log(msg);
                    }
                );
                this.classes[sel_class].projects[sel_project].groups.splice(sel_group, 1);
            },

            // Change preset background -------------------
            change_background: function () {
                $(document.body).removeClass(this.background);
                this.bg_idx++;
                if (this.bg_idx > 2)
                    this.bg_idx = 0;
                this.background = 'bg' + this.bg_idx
                $(document.body).addClass(this.background);
            }
        },
    })
    ;

