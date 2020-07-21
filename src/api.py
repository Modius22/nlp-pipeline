from flask import Flask
from flask import request
from flask_restplus import reqparse, Api, Resource

import control_nlp
import project
import nltk
#################################################################################
# inital
#################################################################################

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
debugging = True


#################################################################################
# API MGMT
#################################################################################

class Loop(Resource):
    def get(self, function):
        """ function for get request via api

        Parameters
        ----------
        function    : str
            name of called function
        """
        if request.args:
            args = request.args
        if function == 'create_project':
            print('this is the function to create a project: ' + args['project_name'])
            project.create_project(args['project_name'])
            print('this is the function to create a project: ' + args['project_name'])
        if function == 'get_project':
           return project.get_project()
        if function == 'get_project_files':
            return project.get_project_files(args['project_name'])
        if function == 'get_file':
            project.get_file(args['project_name'], args['filename'])
            print('this funciton parameteres: ' + args['filename'])
        if function == 'delete_project':
            project.delete_project(args['project_name'])
        return 201


#################################################################################
# Api nlp
#################################################################################

class Nlp(Resource):

    def get(self, project_name, function):
        """ function for get request via api

        Parameters
        ----------
        project_name : str
            name of the project
        function    : str
            name of called function
        """
        args = request.args
        if function == 'exploartion':
            control_nlp.exploartion_data(project_name)
        if function == 'clean':
            control_nlp.clean_data(project_name)
        if function == 'vectorize':
            control_nlp.vectorize_data(project_name)
        if function == 'model':
            control_nlp.model_data(project_name, args['algorithm'])

        return 200

    def post(self, project_name, function):
        """ function to handle post request via api

        Parameters
        ----------
        project_name : str
            name of the project
        function    : str
            name of called function

        """
        args = request.args
        if function == 'load':
            return control_nlp.load_data(project_name, args['text'], args['sentiment'])

        if function == 'predict':
            print('post function if working')
            print(args['algorithm'])
            print(args['text'])

            return control_nlp.prediction_data(project_name, args['algorithm'], args['text'])
        return 200


#################################################################################
# Api route and start
#################################################################################

api.add_resource(Loop, '/nlp/<function>')
api.add_resource(Nlp, '/nlp/<project_name>/<function>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
