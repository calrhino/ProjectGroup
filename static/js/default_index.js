/**
 * Created by jarrett on 11/12/16.
 */

var profile = new Vue({
    el: "#profile",
    delimiters: ['${', '}'],
    unsafeDelimiters: ['!{', '}'],
    data: {
        is_show: false,
        is_edit: false,
        traits: [],
        suggested: []
    },
    methods: {
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
            });
        }
    }
});

var main_content = new Vue({
    el: "#main-content",
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
        contactMember: function (idx) {
            if (idx < 0) {
                //TODO contact all members
            } else {
                //TODO contact specific member
            }
        }
// 2500 durant apt 301

    },
    /*components: {
     'project-template': {
     delimiters: ['${', '}'],
     unsafeDelimiters: ['!{', '}'],
     props: ['data', 'project_idx', 'sel_project'],
     template: "\
     <div>${data.name} ${data.description}\
     <button class='btn' v-on:click='$emit(\"show_more\")'>Show More</button>\
     <div v-for='member in data.members'>\
     ${member}</div>\
     ",
     },
     'class-template': {
     delimiters: ['${', '}'],
     unsafeDelimiters: ['!{', '}'],
     props: ['data', 'class_idx', 'sel_class', 'sel_project'],
     data: function () {
     return {
     name: this.data.name,
     description: this.data.description,
     };
     },
     template: "\
     <div>${name} ${description}\
     <button class='btn' v-on:click='$emit(\"show_more\")'>Show More</button>\
     <div v-if='sel_class==class_idx'><project-template\
     v-for='(project, project_idx) in data.projects'\
     :data='project.data'\
     :project_idx='project_idx'\
     :sel_project='sel_project'\
     v-on:show_more='showProject(class_idx, project_idx)'\
     ></project-template>\
     </div>\
     ",
     }
     }*/
});


/*Vue.component('project-template', {
 props: ['data', 'project_idx', 'sel_project'],
 template: "\
 <div>{{data.name}} {{data.description}}\
 <button class='btn' v-on:click='$emit(\"show_more\")'>Show More</button>\
 <div v-for='member in data.members'>\
 ${member}</div>\
 ",
 });

 Vue.component('class-template', {
 props: ['data', 'class_idx', 'sel_class', 'sel_project'],
 template: "\
 <div>{{data.name}} {{data.description}}\
 <button class='btn' v-on:click='$emit(\"show_more\")'>Show More</button>\
 <div v-if='sel_class==class_idx'><project-template\
 v-for='(project, project_idx) in data.projects'\
 :data='project.data'\
 :project_idx='project_idx'\
 :sel_project='sel_project'\
 v-on:show_more='showProject(class_idx, project_idx)'\
 ></project-template>\
 </div>\
 ",
 });*/

