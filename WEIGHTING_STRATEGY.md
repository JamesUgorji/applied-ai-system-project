# Point-Weighting Strategy - Final Recipe

## Overview
The music recommender uses a **point-weighting system** that scores songs based on how well they match three key user preferences: genre, mood, and energy level.

## Scoring Breakdown

### 1. **Genre Match: +2.0 points** ✓
- **When:** Song's genre exactly matches the user's favorite genre (case-insensitive)
- **Value:** 2.0 points (highest single threshold)
- **Rationale:** Genre is the strongest predictor of recommendation satisfaction

### 2. **Mood Match: +1.0 point** ✓
- **When:** Song's mood exactly matches the user's favorite mood (case-insensitive)
- **Value:** 1.0 point
- **Rationale:** Mood is important but valued less than genre since one genre can serve many moods

### 3. **Energy Similarity: up to +1.0 point** (scaled)
- **How it works:** Linear decay based on distance from target energy
- **Formula:** `points = max(0, 1.0 - |song_energy - user_target_energy|)`
- **Examples:**
  - Song energy = 0.80, target = 0.80 → distance = 0.0 → **+1.0 points**
  - Song energy = 0.90, target = 0.80 → distance = 0.1 → **+0.9 points**
  - Song energy = 0.50, target = 0.80 → distance = 0.3 → **+0.7 points**
  - Song energy = 0.20, target = 0.80 → distance = 0.6 → **+0.4 points**

## Maximum Score
**4.0 points** (2.0 genre + 1.0 mood + 1.0 energy perfect match)

## Recommendation Ranking
- Songs are ranked by total score in **descending order** (highest scores first)
- Ties are broken by song ID for consistency

## Balance Rationale

| Dimension | Points | Why? |
|-----------|--------|------|
| **Genre** | 2.0 | Primary taste indicator, binary match |
| **Mood** | 1.0 | Secondary indicator, adds diversity within genre |
| **Energy** | 1.0 | Contextual fit (workout vs. study vs. sleep) |

### Example Comparisons

**Scenario 1: Perfect Match**
- Song: pop, happy, energy 0.80
- User: favorite_genre="pop", favorite_mood="happy", target_energy=0.80
- Score: 2.0 + 1.0 + 1.0 = **4.0** ⭐

**Scenario 2: Genre & Mood Match, Energy Off**
- Song: pop, happy, energy 0.50
- Score: 2.0 + 1.0 + 0.5 = **3.5**

**Scenario 3: Only Genre Match**
- Song: pop, chill, energy 0.30
- Score: 2.0 + 0.0 + 0.7 = **2.7**

**Scenario 4: Only Energy Match**
- Song: jazz, relaxed, energy 0.80
- Score: 0.0 + 0.0 + 1.0 = **1.0**

## Implementation

### Object-Oriented (Class-based)
```python
recommender = Recommender(songs)
user = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.80
)
recommendations = recommender.recommend(user, k=5)
```

### Functional (Dictionary-based)
```python
songs = load_songs("data/songs.csv")
preferences = {"genre": "pop", "mood": "happy", "energy": 0.80}
recommendations = recommend_songs(preferences, songs, k=5)
# Returns: [(song_dict, score, explanation), ...]
```

## Files Modified
- `src/recommender.py` - Core recommendation logic with scoring
- `demo_weighting_strategy.py` - Interactive demonstration

## Testing
All tests pass with this strategy:
```bash
$ pytest tests/test_recommender.py -v
✓ test_recommend_returns_songs_sorted_by_score
✓ test_explain_recommendation_returns_non_empty_string
```
