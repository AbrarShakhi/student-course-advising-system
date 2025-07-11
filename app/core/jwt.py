from flask_jwt_extended import JWTManager
from datetime import timedelta

# In-memory token blacklist for demonstration (use persistent storage in production)
jwt_blacklist = set()

def init_jwt(app):
    app.config.setdefault('JWT_SECRET_KEY', 'super-secret')  # Change this in production!
    app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', timedelta(hours=1))
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in jwt_blacklist
    return jwt 