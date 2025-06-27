import numpy as np

def regime_vector_distance(a, b):
    """
    Computes cosine distance between two regime probability vectors.
    Inputs are dicts with regime labels and string/float probabilities.
    """
    a_vec = np.array([float(v) for v in a.values()])
    b_vec = np.array([float(v) for v in b.values()])

    dot = np.dot(a_vec, b_vec)
    norm = np.linalg.norm(a_vec) * np.linalg.norm(b_vec)
    cosine_similarity = dot / norm if norm != 0 else 0
    return 1 - cosine_similarity  # distance = 1 - similarity


def score_velocity(history):
    """
    Scores macro regime volatility based on vector drift through time.
    Input: list of historical regime probability snapshots (dicts)
    Returns: float velocity score
    """
    if len(history) < 2:
        return 0.0

    distances = []
    for i in range(len(history) - 1):
        try:
            d = regime_vector_distance(history[i], history[i + 1])
            distances.append(d)
        except Exception as e:
            print(f"Error computing distance at step {i}: {e}")
            continue

    if not distances:
        return 0.0

    return round(sum(distances) / len(distances), 4)
