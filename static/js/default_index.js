/**
 * Created by jarrett on 11/12/16.
 */

var user_profile = new Vue({
    el: "#user_profile",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        is_show: false,
        is_delete: false,
        is_add: false,
        traits: [],
        imglink: '',
        suggested: [],
        trait_field: '',
    },
    methods: {
        toggleViewing: function () {
            this.is_show = !this.is_show;
        },
        toggleDelete: function () {
            this.is_delete = !this.is_delete;
        },
        toggleAdd: function () {
            this.is_add = !this.is_add;
            this.trait_field = '';
        },
        addTrait: function (trait) {
            //TODO communicate submit with database
            $.post(add_trait_url, {
                trait: trait
            }, function (data) {
                this.traits.unshift(data.trait);
            })
        },
        delTrait: function (idx) {
            var trait = this.traits[idx];
            //TODO communicate delete with database
            $.post(del_trait_url, {
                id: trait.id
            }, function (data) {
                this.traits.splice(idx, 1);
            });
        },
        getTraits: function (idx) {
            $getJSON(get_traits_url, function (data) {
                this.traits = data.traits;
                this.imglink = data.imglink;
                this.suggested = data.suggested;
            });
        }
    }
});

var main_content = new Vue({
        el: "#main_content",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            page: 'welcome',
            sel_class: -1,
            sel_project: -1,
            sel_group: -1,
            sel_member: -1,
            is_contact: false,
            user_message: '',
            is_edit_status: false,
            allclasses: [],
            messages: [],
            classes: [
                {
                    name: 'testclass_101',
                    description: 'testing',
                    projects: [
                        {
                            name: 'project1',
                            description: '5 people max',
                            groups: [
                                {
                                    name: 'group11',
                                    description: '1first',
                                    members: [
                                        'potato-chan',
                                        'potaoto-san'
                                    ]
                                },
                                {
                                    name: 'group12',
                                    description: '1second',
                                    members: [
                                        'asdf2',
                                        'fdsa2'
                                    ]
                                }
                            ]
                        },
                        {
                            name: 'project2',
                            description: 'potato',
                            groups: [
                                {
                                    name: 'group21',
                                    description: '2first',
                                    members: [
                                        'potato-chan',
                                        'potaoto-san'
                                    ]
                                },
                                {
                                    name: 'group22',
                                    description: '2second',
                                    members: [
                                        'asdf2',
                                        'fdsa2'
                                    ]
                                }
                            ]
                        }
                    ]
                },
            ]
        },
        methods: {
            extend: function (a, b) {
                for (var i = 0; i < b.length; i++) {
                    a.push(b[i]);
                }
            },


            getClasses: function () {
                $.post(get_classes_url,
                    {}, function (data) {
                        if (data.classes[0] != null)
                            main_content.classes = data.classes;
                    }
                );
            },
            getProjects: function (class_idx) {
                var class_arr = main_content.classes[class_idx];
                $.post(get_projects_url,
                    {
                        class_id: class_arr.id
                    }, function (data) {
                        console.log(data);
                        if (data.projects[0] != null)
                            main_content.extend(class_arr.projects, data.projects);
                    }
                )
            },
            getGroups: function (class_idx, proj_idx) {
                var project = main_content.classes[class_idx].projects[proj_idx];
                $.post(get_groups_url,
                    {
                        project_id: project.id,
                    }, function (data) {
                        console.log(data);
                        if (data.groups[0] != null)
                            main_content.extend(project.groups, data.groups);
                    }
                );
            },
            getMembers: function (class_idx, proj_idx, group_idx) {
                var group = main_content.classes[class_idx].projects[proj_idx].groups[group_idx];
                $.post(get_members_url,
                    {
                        group_id: group.id
                    }, function (data) {
                        console.log(data);
                        if (data.members[0] != null)
                            main_content.extend(group.members, data.members);
                    }
                );
            },
            setGroupStatus: function (class_idx, proj_idx, group_idx) {
                var group = main_content.classes[class_idx].projects[proj_idx].groups[group_idx];
                group._pending = true;
                $.post(set_group_status_url,
                    {
                        group_id: group.id,
                        new_status: group.new_status
                    }, function (data) {
                        console.log(data);
                        group.status = group.new_status;
                        main_content.hideEditStatus();
                        group._pending = false;
                    })
            },
            getAllClasses: function () {
                $.post(get_all_classes_url,
                    {}, function (data) {
                        if (data.classes[0] != null)
                            main_content.allclasses = data.classes;
                    }
                );
            },
            getMessages: function () {
                $.post(get_messages_url,
                    {}, function (data) {
                        if (data.messages[0] != null)
                            main_content.messages = data.messages;
                    });
            },


            setPage: function (page) {
                if (this.page == page) return;
                this.page = page;
                if (page == 'loggedin')
                    this.getClasses();
                else if (page == 'joinclass')
                    this.getAllClasses();
                else if (page == 'mymessages')
                    this.getMessages();
            },

            //Functions to Control Visuals
            toggleClass: function (class_idx) {
                if (this.sel_class == class_idx)
                    this.hideClass();
                else {
                    if (this.classes[class_idx].projects[0] == null) {
                        this.getProjects(class_idx);
                    }
                    this.sel_class = class_idx;
                }
            },
            toggleProject: function (proj_idx, class_idx) {
                if (this.sel_project == proj_idx)
                    this.hideProject();
                else {
                    if (this.classes[class_idx].projects[proj_idx].groups[0] == null) {
                        this.getGroups(class_idx, proj_idx);
                    }
                    this.sel_project = proj_idx;
                }
            },
            toggleGroup: function (group_idx, proj_idx, class_idx) {
                if (this.sel_group == group_idx)
                    this.hideGroup();
                else {
                    if (this.classes[class_idx].projects[proj_idx].groups[group_idx].members[0] == null) {
                        this.getMembers(class_idx, proj_idx, group_idx);
                    }
                    this.sel_group = group_idx;
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
            showContact: function () {
                this.is_contact = true;
            },
            hideClass: function () {
                this.sel_class = -1;
                this.hideProject();
            },
            hideProject: function () {
                this.sel_project = -1;
                this.hideGroup();
            },
            hideGroup: function () {
                this.sel_group = -1;
                this.showAllMember();
                this.hideContact();
                this.hideEditStatus();
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


            contactMembers: function (class_idx, project_idx, group_idx) {
                var members = this.classes[class_idx].projects[project_idx].groups[group_idx].members;
                if (this.sel_member < 0) {
                    for (var i = 0, len = members.length; i < len; i++) {
                        contact_member(members[i], this.user_message)
                    }
                } else {
                    contact_member(members[this.sel_member], this.user_message);
                }
                this.hideContact();
            },

            join_class: function (class_idx) {
                join_class(this.allclasses[class_idx].id)
            },
        },
    })
    ;

