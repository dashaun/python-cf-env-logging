# import dependencies
import os
import json
import logging
import sys
from flask import Flask
from flask import Response
from cfenv import AppEnv

# Configure logging
logging.basicConfig(
    stream=sys.stdout,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=logging.INFO
)

# Bootstrap flask and cf-env
app = Flask(__name__)
env = AppEnv()

# Port 3000 when running locally, or get the port from cf-env
if env.port is None:
    port = 3000
else:
    port = env.port


# Route which returns a string using values from cf-env
@app.route('/')
def hello_world():
    logging.info("hello_world")
    return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0) + ' of ' + env.name)


# Route that answers the health endpoint for cloud foundry
@app.route('/health')
def health():
    ret = {'status': 'UP'}
    logging.info("health")
    return Response(json.dumps(ret), mimetype='application/json')


# Starts the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
