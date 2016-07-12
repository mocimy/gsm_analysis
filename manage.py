# Set the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from gsm_analysis import app

manager = Manager(app)


manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='127.0.0.1',
    port=5001)
)

if __name__ == "__main__":
    manager.run()
