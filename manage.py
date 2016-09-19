from flask_script import Manager

from campbellsoup import create_application

manager = Manager(create_application)
manager.add_option('-c', '--config', dest='config')

if __name__ == '__main__':
    manager.run()
