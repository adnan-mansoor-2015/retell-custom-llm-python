from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class DBClient:

    def __init__(self):
        # Initialize Qdrant and embedding model
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def load_menu(self):
        # Define menu items
        menu = [
            {"name": "Margherita Pizza", "description": "Classic pizza with tomato, mozzarella, and basil", "price": 8.99},
            {"name": "Pepperoni Pizza", "description": "Pizza topped with pepperoni slices", "price": 9.99},
            {"name": "Coke", "description": "Chilled soft drink", "price": 1.99},
        ]

        # Create collection in Qdrant
        self.client.recreate_collection(
            collection_name="menu",
            vector_size=384,  # Dimension of your embeddings
            distance="Cosine"  # Use cosine similarity
        )

        # Insert menu items
        for item in menu:
            embedding = self.model.encode(item["name"])  # Create vector
            self.client.upsert(
                collection_name="menu",
                points=[
                    {
                        "id": item["name"],
                        "vector": embedding,
                        "payload": item  # Store metadata (name, description, price)
                    }
                ]
            )

def query_menu(self, query):
    # Create embedding for the query
    query_vector = self.model.encode(query)

    # Search the vector database
    results = self.client.search(
        collection_name="menu",
        query_vector=query_vector,
        limit=1,  # Return top 1 match
        with_payload=True  # Include metadata
    )

    # Return the best match
    if results:
        return results[0].payload
    return "Sorry, I couldn't find that on the menu."