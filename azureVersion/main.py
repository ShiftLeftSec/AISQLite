from frontend import frontend_ai
from middleware import run_zap
from backend import backend_ai
from backend import XML_to_db

frontend_ai.frontend()
run_zap.startzap()
XML_to_db.xml_to_db()
backend_ai.query_and_graph()