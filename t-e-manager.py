__author__ = 'Cedric Da Costa Faro'

from app import create_app, db
from app.models import User, Role, Task, Project, Client, Currency, Category, CategoryType

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Task': Task, 'Role': Role, 'Project': Project, 'Currency': Currency,
            'Client': Client, 'Category': Category, 'CategoryType': CategoryType}
