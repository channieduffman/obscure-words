from flask import Flask
import os

def create_app(test_config=None):
    # define app instance and default config
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'obscurew.sqlite') 
    )

    # load correct config definitions
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # create instance folder if not exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # test route
    @app.route('/hello')
    def hello():
        return 'Hello from Obscure Words!'
    
    from . import db
    db.init_app(app)

    from . import words
    app.register_blueprint(words.bp)
    app.add_url_rule('/', view_func=words.index)

    return app