from flask import g, abort

def admin_required(f):
    """Декоратор для перевірки адміністративного доступу."""
    def wrapper(*args, **kwargs):
        if not getattr(g, "is_admin", False):  # Перевіряємо прапорець is_admin
            abort(403, description="Доступ заборонено: лише для адміністраторів.")
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper