
"""
Simple flask thing
"""

from app import app
from app.modules.static import Static
from app.modules.backend import Backend
from app.modules.auth import Auth
from app.modules.backend.modules.page import Backend_Page
from app.modules.backend.modules.file import Backend_File
from app.modules.backend.modules.user import Backend_User

app.register_blueprint(Auth)
app.register_blueprint(Static)
app.register_blueprint(Backend, url_prefix='/backend')
app.register_blueprint(Backend_Page, url_prefix='/backend/page')
app.register_blueprint(Backend_File, url_prefix='/backend/file')
app.register_blueprint(Backend_User, url_prefix='/backend/user')
