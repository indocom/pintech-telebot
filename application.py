import os

from flask import Flask

from main import main

application = Flask(__name__)


@application.route('/')
def heartbeat():
    return "Still Active"


@application.route('/start')
def start():
    main()
    return "Application has started"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(debug=True, host='0.0.0.0', port=port)
