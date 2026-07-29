import importlib
import pkgutil

COMMAND_HANDLERS = []

def command(name):
    """Decorator: registers a function as a /command handler."""
    def wrapper(func):
        COMMAND_HANDLERS.append((name, func))
        return func
    return wrapper

def load_all():
    """Imports every module in commands/ so their @command decorators run."""
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name != "__init__":
            importlib.import_module(f"{__name__}.{module_name}")