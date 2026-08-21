from sentence_transformers import SentenceTransformer

# Load the model globally so it only loads into memory once.
# 'all-MiniLM-L6-v2' is the gold standard for fast, lightweight semantic similarity.
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list[float]:
    """
    Takes a string of text and returns a dense vector embedding.
    We convert the numpy array to a standard Python list of floats 
    so it can be easily stored in the database as JSON or an Array.
    """
    # The encode method does the heavy lifting of turning text into math
    vector = model.encode(text)
    
    return vector.tolist()