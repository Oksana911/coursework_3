from project.config import config
from project.server import create_app


if __name__ == '__main__':
    application = create_app(config)
    application.run(port=25000)
