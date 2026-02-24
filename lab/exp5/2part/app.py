import os
from flask import Flask

app = Flask(__name__)

@app.route('/config')
def config():
    return {
        'db_host': os.environ.get('DATABASE_HOST', 'localhost'),
        'debug': os.environ.get('DEBUG', 'false'),
        'port': os.environ.get('PORT', '5000')
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))