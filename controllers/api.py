@auth.requires_login()
def get_classes():
    """get the classes associated with a student"""
    student = get_student(request.vars.auth_id)
    classes = db(db.stud_classes.student_id==student.id).select()
    response_classes = []
    for i, c in enumerate(classes):
        response_classes.append(response_class(c))
    return response.json(dict(classes=response_classes))


@auth.requires_login()
def get_projects():
    """get the projects associated with a class"""
    projects = db(db.projects.class_id==request.vars.class_id).select()
    response_projects = []
    for i, p in enumerate(projects):
        response_projects.append(response_project(p))
    return response.json(dict(projects=response_projects))


@auth.requires_login()
def get_students():
    """get the students associated with a project"""
    students = db(db.proj_students.project_id==request.vars.project_id).select()
    response_students = []
    for i, s in enumerate(students):
        response_students.append(response_student(s))
    return response.json(dict(students=response_students))


# database insert and delete ------------------

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


@auth.requires_login()
def create_class():
    """create a class to the database"""
    name = request.vars.name
    description = request.vars.description
    instructor = get_student(request.vars.auth_id)

    class_id = db.classes.insert(name=name, description=description, instructor_id=instructor.id)
    db.stud_classes.insert(student_id=instructor.id, class_id=class_id)
    return response.json('create class success')


@auth.requires_login()
def join_class():
    """a student joins a class"""
    class_id = request.vars.class_id
    student = get_student(request.vars.auth_id)
    db.stud_classes.insert(student_id=student.id, class_id=class_id)
    return response.json('add class success')


@auth.requires_login()
def leave_class():
    """a student leaves a class"""
    class_id = request.vars.class_id
    student = get_student(request.vars.auth_id)
    db(db.stud_classes.student_id == student.id and db.stud_classes.class_id == class_id).delete()
    return response.json('leave class success')


@auth.requires_login()
def delete_class():
    """delete a class"""
    class_id = request.vars.class_id
    db(db.classes.id == class_id).delete()
    return response.json('delete class success')


@auth.requires_login()
def create_project():
    """a student creates a project in the database"""
    class_id = request.vars.class_id
    name = request.vars.name
    description = request.vars.description
    leader = get_student(request.vars.auth_id)

    project_id = db.projects.insert(name=name, description=description, leader_id=leader.id, class_id=class_id)
    db.proj_students.insert(student_id=leader.id, project_id=project_id)
    return response.json('create project success')


@auth.requires_login()
def join_project():
    """a student joins a project"""
    project_id = request.vars.project_id
    student = get_student(request.vars.auth_id)
    db.proj_students.insert(student_id=student.id, project_id=project_id)
    return response.json('join project success')

@auth.requires_login()
def leave_project():
    """a student leaves a project"""
    project_id = request.vars.project_id
    student = get_student(request.vars.auth_id)
    db(db.proj_students.project_id==project_id and db.proj_students.student_id==student.id).delete()

    if (db(db.proj_students.project_id == project_id).select() is None):
        db(db.projects.id == project_id).delete()
        return response.json('leave and remove project success')
    return response.json('leave project success')

def get_student(auth_id):
    return db(db.students.google_auth_id == auth_id).select().first()


# helper methods to ensure proper dictionary is sent to client
def response_class(c):
    return dict(
        id=c.id,
        description=c.description,
        name=c.name,
        projects=[],
    )


def response_project(p):
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
