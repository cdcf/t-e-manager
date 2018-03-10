Time Tracker and Expense Manager app for Freelance
==================================================

I have designed and created this app to track my freelance activity, with a split per client, projects and tasks.\
There is also a section related to Expenses Management, linked with a mobile app. From the mobile app, we can scan 
an expense and add it to a project.\
Note that the Expense Management section is under development and will be soon available, as well as the mobile app.

Requirements
------------

- Python 3.6
- virtualenv (or venv if you are using Python 3.6)
- git
- Java, to use Elasticsearch

Setup
-----

**Step 1**: Clone the git repository

    $ git clone https://github.com/cdcf/t-e-manager.git
    $ cd t-e-manager

**Step 2**: Create a virtual environment.

For Linux, OSX or any other platform that uses *bash* as command prompt (including Cygwin on Windows):

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are using Python 3.x:

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

For Windows users working on the standard command prompt:

    > virtualenv venv
    > venv\scripts\activate
    (venv) > pip install -r requirements.txt

**Step 3**: Run the initial database migration:

    (venv) $ export FLASK_APP=t-e-manager.py
    (venv) $ flask db init
    (venv) $ flask db migrate -m "initial migration"
    (venv) $ flask db upgrade
     
**Step 4**: Start the application:

    (venv) $ flask run
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Now open your web browser and type [http://localhost:5000](http://localhost:5000) in the address bar to see the
application running.

**Step 5**: Create an administrator user

Open another terminal session within the virtual env

    (venv) $ flask shell        # this is run a Python shell with an access to the app files
    >>> Role.insert_roles()     # this will add the different roles into the database
    >>> Role.query.all()        # this will list the roles inserted in the database so you can pick one when creating the admin role
    [<Role User>, <Role Moderator>, <Role Administrator>]

In your browser, use the url [http://localhost:5000/register_admin.html](http://localhost:5000/register_admin.html)



If you need to add non-admin users, you can now do it from the visible link "Register" in the top right corner of the app.
