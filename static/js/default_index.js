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
        google_auth: false,
        auth_id: '',
        sel_class: -1,
        sel_project: -1,
        sel_member: -1,
        is_contact: false,
        user_message: '',
        classes: [
            {
                name: 'testclass_101',
                description: 'testing',
                projects: [
                    {
                        name: 'project11',
                        description: '1first',
                        members: [
                            'potato-chan',
                            'potaoto-san'
                        ]
                    },
                    {
                        name: 'project12',
                        description: '1second',
                        members: [
                            'asdf2',
                            'fdsa2'
                        ]
                    }
                ]
            },
            {
                name: 'testclass_007',
                description: 'secret_spy',
                projects: [
                    {
                        name: 'project-goldeneye',
                        description: 'thing',
                        members: [
                            'bond'
                        ]
                    },
                    {
                        name: 'project-casino',
                        description: 'boom',
                        members: [
                            'bond'
                        ]
                    }
                ]
            },
        ]
    },
    methods: {
        setPage: function (page) {
            if (this.page == page) return;
            this.page = page;
        },

        //Functions to Control Visuals
        toggleClass: function (idx) {
            if (this.sel_class == idx)
                this.sel_class = -1;
            else
                this.sel_class = idx;
        },
        toggleProject: function (idx) {
            if (this.sel_project == idx)
                this.sel_project = -1;
            else
                this.sel_project = idx;
        },
        toggleMember: function (idx) {
            if (this.sel_member == idx)
                this.sel_member = -1;
            else
                this.sel_member = idx;
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
            this.showAllMember();
            this.hideContact();
        },
        showAllMember: function () {
            this.sel_member = -1;
        },
        hideContact: function () {
            this.is_contact = false;
            this.clearMessage();
        },
        clearMessage: function () {
            this.user_message = '';
        },

        getClasses: function(auth_id) {
            $.post(get_classes_url,
                {
                    auth_id:auth_id,
                }, function(data) {
                    console.log(data);
                }
            );
        },
        getProjects: function(class_id) {
            $.post(get_projects_url,
                {
                    class_id:class_id,
                }, function(data) {
                    console.log(data);
                }
            );
        },
        getStudents: function(project_id) {
            $.post(get_students_url,
                {
                    project_id:project_id
                }, function(data) {
                    console.log(data);
                }
            );
        },
        contactMember: function (idx) {
            if (idx < 0) {
                //TODO contact all members
            } else {
                //TODO contact specific member
            }
        }
    },
});

