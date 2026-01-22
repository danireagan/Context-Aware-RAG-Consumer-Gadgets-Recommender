from flask import render_template, Flask, request, Response
from prometheus_client import Counter, generate_latest
from rag_pipeline.rag_chain import RAGChainBuilder
from rag_pipeline.data_ingestor import DataIngestor

from dotenv import load_dotenv

load_dotenv()

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

def create_app():

    app = Flask(__name__)

    vector_store = DataIngestor().ingest_data(load_existing=True)
    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def index ():
        REQUEST_COUNT.inc()
        return render_template('index.html')

    @app.route("/get", methods=["POST"])
    def get_response():
        REQUEST_COUNT.inc()
        user_input = request.form["msg"]
        session_id = request.cookies.get("session_id", "user_session")

        response = rag_chain.invoke({"input": user_input},
        config={"configurable": {"session_id": session_id}})

        return response["answer"]
    
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug = True)