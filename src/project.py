import os
import json
import shutil

#################################################################################
# project management
#################################################################################

def create_project(project):
    """ create project folder in working directory

    Parameters
    ----------
    project : str
        name of the project
    """
    try:
        path = os.getcwd() + '/../working/' + project
        print(path)
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def get_project():
    """ get all project by project folder

    Returns
    -------

    """
    os.chdir('../working/')
    path = '.'
    subdirs = [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]
    return json.dumps(subdirs)

def get_project_files(project):
    """ get all files of a project

    Parameters
    ----------
    project : str
        name of the project
    """
    path = os.getcwd() + '/../working/' + project + '/'
    folders = []

    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(os.path.join(r, folder))
    mylist = []

    for s in f:
        mylist.append(s)

    return json.dumps(mylist)


def delete_project(project):
    """ delete a project folder

    Parameters
    ----------
    project : str
        name of the project
    """
    try:
        path = os.getcwd() + '/../working/' + project
        shutil.rmtree(path)
        print("Directory '%s' has been removed successfully" % project)
    except OSError as error:
        print(error)
        print("Directory '%s' can not be removed" % project)
