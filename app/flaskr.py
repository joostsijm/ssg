
"""
Simple flask thing
"""

from app import app
from app.modules.static import Static
from app.modules.backend import Backend
from app.modules.auth import Auth
from app.modules.backend.modules.page import Backend_Page

app.register_blueprint(Auth)
app.register_blueprint(Static)
app.register_blueprint(Backend, url_prefix='/backend')
app.register_blueprint(Backend_Page, url_prefix='/backend/page')
