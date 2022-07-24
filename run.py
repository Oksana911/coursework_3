from project.config import config
from project.server import create_app
from flask_restx import Api


api = Api(
    authorizations={
        'Bearer': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}
    },
    title="Flask Course Project 3",
    doc="/docs"
    )


if __name__ == '__main__':
    application = create_app(config)
    application.run(port=25000)




# @app.shell_context_processor
# def shell():
#     return {
#         "db": db,
#         "Genre": Genre,
#     }
