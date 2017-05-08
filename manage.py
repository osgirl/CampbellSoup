# (c) 2016 Julian Gonggrijp

from flask_script import Manager
from flask_migrate import MigrateCommand

from campbellsoup import create_application
from campbellsoup.import_command import import_manager

manager = Manager(create_application)
manager.add_option('-c', '--config', dest='config')
manager.add_command('db', MigrateCommand)
manager.add_command('archive', import_manager)

if __name__ == '__main__':
    manager.run()
