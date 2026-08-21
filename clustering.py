import torch
from sentence_transformers import util

# The similarity threshold determines how strict the grouping is.
# 0.85 is a solid starting point for the MiniLM model.
# 1.0 means exact match, 0.0 means completely unrelated.
SIMILARITY_THRESHOLD = 0.85

def find_best_cluster(new_embedding: list[float], existing_tickets) -> int | None:
    """
    Compares a new ticket's embedding against existing tickets.
    Returns the cluster_id of the best match if it exceeds the threshold,
    otherwise returns None.
    """
    if not existing_tickets:
        return None

    # Convert the new embedding from a Python list into a PyTorch tensor
    new_tensor = torch.tensor(new_embedding)

    best_score = 0.0
    best_cluster_id = None

    for ticket in existing_tickets:
        # Check if embedding is None to avoid Numpy evaluation errors
        if ticket.embedding is None or ticket.cluster_id is None:
            continue
            
        # Convert the existing ticket's embedding to a tensor
        existing_tensor = torch.tensor(ticket.embedding)
        
        # Calculate cosine similarity between the two vectors
        # util.cos_sim returns a 2D tensor, so we use .item() to grab the raw float value
        score = util.cos_sim(new_tensor, existing_tensor).item()
        
        if score > best_score:
            best_score = score
            best_cluster_id = ticket.cluster_id

    # If our best match is higher than our threshold, we found a duplicate cluster!
    if best_score >= SIMILARITY_THRESHOLD:
        return best_cluster_id
        
    return None