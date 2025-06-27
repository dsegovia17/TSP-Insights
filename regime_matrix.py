import numpy as np
from sklearn.preprocessing import StandardScaler

def normalize_pillars(pillars: dict) -> list:
    """
    Z-scores the macro pillar vector to handle scale and directional sensitivity.
    Prevents zero variance blowups by returning a neutral vector if needed.
    """
    scores = np.array(list(pillars.values())).reshape(1, -1)
    if np.all(scores == scores[0]):  # constant vector: no variance
        return [0 for _ in range(scores.shape[1])]
    scaler = StandardScaler()
    z_scores = scaler.fit_transform(scores)[0]
    return z_scores.tolist()

def regime_profiles() -> dict:
    """
    Archetypal macro regimes for directional matching
    """
    return {
        "Expansion":   [ 1,  1,  1,  1,  1,  1],
        "Recovery":    [ 1, -1,  1,  1,  0,  0],
        "Neutral":     [ 0,  0,  0,  0,  0,  0],
        "Contraction": [-1, -1, -1, -1,  0, -1],
        "Crisis":      [-1, -1, -1, -1, -1, -1]
    }

def cosine_similarity(a: list, b: list) -> float:
    """
    Robust cosine similarity between two vectors
    """
    a, b = np.array(a), np.array(b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(a, b) / (norm_a * norm_b)

def classify_regime(pillars: dict) -> dict:
    """
    Transforms the macro pillar vector into:
    - Soft regime probability distribution
    - A stability/confidence score
    """
    norm_vector = normalize_pillars(pillars)
    profiles = regime_profiles()

    similarities = {
        name: cosine_similarity(norm_vector, profile)
        for name, profile in profiles.items()
    }

    # Normalize non-negative similarities into probabilities
    total = sum(max(s, 0) for s in similarities.values()) or 1e-9
    probabilities = {
        name: round(max(score, 0) / total, 4)
        for name, score in similarities.items()
    }

    top_two = sorted(probabilities.values(), reverse=True)
    stability = round(top_two[0] - top_two[1], 4) if len(top_two) >= 2 else 0.0

    return {
        "probabilities": probabilities,
        "stability": stability
    }
