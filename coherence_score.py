import numpy as np

def score_coherence(pillars: dict) -> float:
    """
    Measures directional alignment between macro pillars.
    Outputs a coherence score from 0 (chaos) to 1 (fully aligned).
    """

    values = np.array(list(pillars.values()))
    if len(values) == 0:
        return 0

    vector = values / (np.linalg.norm(values) + 1e-9)  # normalize
    dot_matrix = np.outer(vector, vector)
    coherence = dot_matrix.mean()

    return round(coherence, 4)
