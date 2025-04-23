import frontend
import frontend.frontend_ai
from middleware import run_zap
from backend import backend_ai

frontend.frontend_ai.frontend()
run_zap.startzap()
backend_ai.XML_to_db()
backend_ai.backend_ai.query_and_graph()