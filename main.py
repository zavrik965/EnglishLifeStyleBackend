from flask import Flask
import uuid
from admin.admin import admin

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.secret_key = uuid.uuid4().hex
app.run(host="0.0.0.0", debug=True)
