import numpy as np

def regime_vector_distance(a: dict, b: dict) -> float:
    """
    Cosine distance between two regime probability vectors
    """
    keys = list(a.keys())
    a_vec = np.array([a[k] for k in keys])
    b_vec = np.array([b[k] for k in keys])

    dot = np.dot(a_vec, b_vec)
    norms = np.linalg.norm(a_vec) * np.linalg.norm(b_vec)
    return 1 - dot / (norms + 1e-9)

def score_velocity(history: list[dict]) -> float:
    """
    Measures average regime vector change over last N periods
    """
    if len(history) < 2:
        return 0.0

    distances = [
        regime_vector_distance(history[i], history[i+1])
        for i in range(len(history)-1)
    ]
    velocity = sum(distances) / len(distances)
    return round(velocity, 4)

def flag_fragility(velocity_score: float, threshold: float = 0.6) -> bool:
    return velocity_score > threshold
