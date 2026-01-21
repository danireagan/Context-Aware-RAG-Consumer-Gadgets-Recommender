from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from rag_pipeline.data_converter import DataConverter
from rag_pipeline.config import Config

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vector_store = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="gadgets_db",
            token =Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE,
            api_endpoint =Config.ASTRA_DB_API_ENDPOINT
        )
    
    def ingest_data(self, load_existing: bool = True):
        if load_existing:
            return self.vector_store
        
        data_converter = DataConverter(file_path="data/ConsumerGadgets.csv")
        documents = data_converter.csv_to_documents()

        self.vector_store.add_documents(documents)

        return self.vector_store

if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest_data(load_existing=False)