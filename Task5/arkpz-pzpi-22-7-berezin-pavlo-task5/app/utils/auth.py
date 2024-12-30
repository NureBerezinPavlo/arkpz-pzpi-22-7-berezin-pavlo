from functools import wraps
from app.routes.admins import Admin
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def admin_required(fn):
    """Декоратор для перевірки адміністративного доступу."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # Перевірка токена
        admin_id = get_jwt_identity() # Витяг ідентифікатора адміністратора з токена

        # Перевірка, чи існує адміністратор з таким ID
        admin = Admin.query.get(admin_id)
        if not admin:
            return {"message": "Доступ заборонено: лише для адміністраторів."}, 403
        return fn(*args, **kwargs)
    return wrapper