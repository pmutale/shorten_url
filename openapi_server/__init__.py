import connexion
from flask_cors import CORS

from openapi_server import url_encoder

app = connexion.App(__name__, specification_dir='./openapi/')
app.add_api('openapi.yaml',
            arguments={'title': 'API: Shorten URL'},
            pythonic_params=True)
app.app.json_encoder = url_encoder.JSONEncoder
CORS(app.app)
