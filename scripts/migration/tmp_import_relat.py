import importlib
import traceback

try:
    m = importlib.import_module("atividades.views_ext.relatorios")
    print("import ok", m.__name__)
except Exception:
    traceback.print_exc()
