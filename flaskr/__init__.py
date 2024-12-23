import os
# for paths to system directories
from flask import Flask
#import flask application object
from . import db
from . import auth


#this function is known as application factory because it will be dealing with
#app configuration, registration and setup 

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #__name__ is the name of the current python module, second argument is used so that the local data should not be commited to version control
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.splite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page route for testing
    @app.route('/hello')
    def hello():
        return "Start flask Project Testing"
    
    db.init_app(app)
    # create/connect to database, open database file, run commands and close
    app.register_blueprint(auth.bp)
    # registering authentication blueprint
    
    return app
