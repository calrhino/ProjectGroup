# database retrieve information for client ------

@auth.requires_login()
def get_classes():
    """get the classes associated with a student"""
    # select all relations between students and classes for particular student
    student = get_student(request.vars.auth_id)
    classes = db(db.class_students.student_id==student.id).select()
    response_classes = []
    # get class from each relation (classes of student)
    for i, cref in enumerate(classes):
        response_classes.append(response_class(cref.class_id))
    return response.json(dict(classes=response_classes))


@auth.requires_login()
def get_groups():
    """get the groups associated with a class"""
    # select all groups for a class
    groups = db(db.groups.class_id==request.vars.class_id).select()
    response_groups = []
    # groups are only associated to one class per
    for i, p in enumerate(groups):
        response_groups.append(response_group(p))
    return response.json(dict(groups=response_groups))


@auth.requires_login()
def get_students():
    """get the students associated with a group"""
    # select all relations between groups and students for particular group
    students = db(db.group_students.group_id==request.vars.group_id).select()
    response_students = []
    # get student from each relation (members of group)
    for i, sref in enumerate(students):
        response_students.append(response_student(sref.student_id))
    return response.json(dict(students=response_students))

# database insert and delete --------------------

@auth.requires_login()
def add_student():
    """add a new student to the database"""
    auth_id = request.vars.auth_id
    db.students.insert(google_auth_id=auth_id)
    return response.json('add student success')


@auth.requires_login()
def delete_student():
    """delete a student from the database"""
    auth_id = request.vars.auth_id
    db(db.students.google_auth_id == auth_id).delete()
    return response.json('delete student success')

# class api calls -------------------------------
@auth.requires_login()
def create_class():
    """a student creates a class and is the 'instructor'"""
    name = request.vars.name
    description = request.vars.description
    instructor = get_student(request.vars.auth_id)

    class_id = db.classes.insert(name=name, description=description, instructor_id=instructor.id)
    db.class_students.insert(student_id=instructor.id, class_id=class_id)
    return response.json('create class success')

@auth.requires_login()
def join_class():
    """a student joins a project"""
    class_id = request.vars.class_id
    student = get_student(request.vars.auth_id)
    db.class_students.insert(student_id=student.id, class_id=class_id)
    return response.json('add class success')


@auth.requires_login()
def leave_class():
    """a student leaves a class"""
    class_id = request.vars.class_id
    student = get_student(request.vars.auth_id)
    db(db.class_students.student_id == student.id and db.class_students.class_id == class_id).delete()
    return response.json('leave class success')

@auth.requires_login()
def delete_class():
    """delete a class"""
    class_id = request.vars.class_id
    db(db.classes.id == class_id).delete()
    return response.json('delete class success')

# project api calls -----------------------------
@auth.requires_login()
def create_project():
    """only instructor of class may create project"""
    class_id = request.vars.class_id
    instructor = get_student(request.vars.auth_id)
    if (instructor is not db(db.classes.id == class_id).select().first().student_id):
        return response.json('invalid; not instructor')
    name = request.vars.name
    description = request.vars.description

    project_id = db.projects.insert(name=name, description=description, class_id=class_id)
    return response.json('create class success')

@auth.requires_login()
def join_project():
    """a student joins a project"""
    project_id = request.vars.project_id
    student = get_student(request.vars.auth_id)
    db.proj_students.insert(student_id=student.id, project_id=project_id)
    return response.json('add class success')

@auth.requires_login()
def leave_project():
    """a student leaves a project"""
    project_id = request.vars.project_id
    student = get_student(request.vars.auth_id)
    db(db.proj_students.student_id == student.id and db.proj_students.project_id == project_id).delete()
    return response.json('leave class success')


@auth.requires_login()
def delete_project():
    """delete a project"""
    project_id = request.vars.project_id
    db(db.projects.id == project_id).delete()
    return response.json('delete class success')

# group api calls -------------------------------
@auth.requires_login()
def create_group():
    """a student creates a group and is the 'leader'"""
    project_id = request.vars.project_id
    name = request.vars.name
    description = request.vars.description
    leader = get_student(request.vars.auth_id)

    group_id = db.groups.insert(name=name, description=description, leader_id=leader.id, class_id=class_id)
    db.group_students.insert(student_id=leader.id, group_id=group_id)
    return response.json('create group success')

@auth.requires_login()
def join_group():
    """a student joins a group"""
    group_id = request.vars.group_id
    student = get_student(request.vars.auth_id)
    db.group_students.insert(student_id=student.id, group_id=group_id)
    return response.json('join group success')

@auth.requires_login()
def leave_group():
    """a student leaves a group and autodetect 0 members for deletion"""
    group_id = request.vars.group_id
    student = get_student(request.vars.auth_id)
    db(db.group_students.group_id==group_id and db.group_students.student_id==student.id).delete()

    print db(db.group_students.group_id == group_id).select()
    if (db(db.group_students.group_id == group_id).select() is None):
        db(db.groups.id == group_id).delete()
        return response.json('leave and remove group success')
    return response.json('leave group success')

@auth.requires_login()
def delete_group():
    """delete a class"""
    group_id = request.vars.group_id
    db(db.groups.id == group_id).delete()
    return response.json('delete class success')

# get student for google_auth_id
def get_student(auth_id):
    return db(db.students.google_auth_id == auth_id).select().first()


# helper methods to ensure proper dictionary is sent to client
def response_class(c):
    return dict(
        id=c.id,
        description=c.description,
        name=c.name,
        groups=[],
    )


def response_group(p):
    return dict(
        id=p.id,
        description=p.description,
        name=p.name,
        students=[]
    )


def response_student(s):
    return dict(
        auth_id=s.google_auth_id,
    )

def pr(msg):
    print(msg)
