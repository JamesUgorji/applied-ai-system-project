from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import csv
from difflib import SequenceMatcher

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # ===== FIX #2: Energy Tolerance =====
    energy_tolerance: float = 0.2  # Acceptance range around target energy (±0.2)
    # ===== FIX #3: Extended Song Features =====
    target_danceability: Optional[float] = None  # Prefer danceable songs (0-1)
    danceability_weight: float = 0.0  # How much to weight danceability (0-1)
    target_valence: Optional[float] = None  # Prefer positive/uplifting (0-1)
    valence_weight: float = 0.0  # How much to weight valence (0-1)
    acoustic_weight: float = 0.0  # How much to weight acousticness (0-1)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    # ===== UPDATED WEIGHTS: Double Energy, Half Genre =====
    # Original: Genre 1.5, Mood 1.0, Energy 1.0 (max: 3.5)
    # New:      Genre 0.75, Mood 1.0, Energy 2.0 (max: 3.75)
    # Importance distribution: Genre 20%, Mood 27%, Energy 53%
    GENRE_MATCH_POINTS = 0.75      # Halved from 1.5
    GENRE_FUZZY_POINTS = 0.375     # Halved from 0.75 (fuzzy match)
    MOOD_MATCH_POINTS = 1.0        # Unchanged
    MOOD_FUZZY_POINTS = 0.5        # Unchanged (fuzzy match)
    ENERGY_MAX_POINTS = 2.0        # Doubled from 1.0
    FEATURE_POINTS = 0.5           # Max points for danceability/valence/acousticness

    def __init__(self, songs: List[Song]):
        self.songs = songs
    
    def _fuzzy_match(self, user_pref: str, song_attr: str, threshold: float = 0.7) -> Tuple[float, str]:
        """
        FIX #4: Fuzzy matching for genres/moods.
        Returns (match_score, match_type) where match_score is 0, 0.5, or 1.0
        - 1.0 = exact match
        - 0.5 = fuzzy match (similarity > threshold)
        - 0.0 = no match
        """
        user_lower = user_pref.lower().strip()
        song_lower = song_attr.lower().strip()
        
        # Exact match
        if user_lower == song_lower:
            return (1.0, "exact")
        
        # Fuzzy match using SequenceMatcher
        similarity = SequenceMatcher(None, user_lower, song_lower).ratio()
        if similarity >= threshold:
            return (0.5, f"fuzzy({similarity:.2f})")
        
        return (0.0, "no_match")

    def calculate_score(self, user: UserProfile, song: Song) -> float:
        """
        Enhanced scoring with fuzzy matching, energy tolerance, and extended features.
        Fixes: (#1) reduced genre weight, (#2) energy tolerance, (#3) extended features, (#4) fuzzy matching
        """
        score = 0.0
        
        # ===== FIX #4: Fuzzy Matching for Genre =====
        genre_match, genre_type = self._fuzzy_match(user.favorite_genre, song.genre)
        if genre_match == 1.0:
            score += self.GENRE_MATCH_POINTS
        elif genre_match == 0.5:
            score += self.GENRE_FUZZY_POINTS
        
        # ===== FIX #4: Fuzzy Matching for Mood =====
        mood_match, mood_type = self._fuzzy_match(user.favorite_mood, song.mood)
        if mood_match == 1.0:
            score += self.MOOD_MATCH_POINTS
        elif mood_match == 0.5:
            score += self.MOOD_FUZZY_POINTS
        
        # ===== FIX #2: Energy Similarity with Tolerance =====
        # Uses energy_tolerance to determine acceptance range
        energy_distance = abs(song.energy - user.target_energy)
        if energy_distance <= user.energy_tolerance:
            # Within tolerance: linear scoring from full points down to threshold
            energy_similarity = 1.0 - (energy_distance / user.energy_tolerance)
        else:
            # Outside tolerance: exponential decay
            excess_distance = energy_distance - user.energy_tolerance
            energy_similarity = max(0.0, 1.0 - excess_distance)
        score += energy_similarity * self.ENERGY_MAX_POINTS
        
        # ===== FIX #3: Extended Song Features =====
        # Danceability preference
        if user.target_danceability is not None and user.danceability_weight > 0:
            dance_distance = abs(song.danceability - user.target_danceability)
            dance_similarity = max(0.0, 1.0 - dance_distance)
            score += dance_similarity * self.FEATURE_POINTS * user.danceability_weight
        
        # Valence (positivity) preference
        if user.target_valence is not None and user.valence_weight > 0:
            valence_distance = abs(song.valence - user.target_valence)
            valence_similarity = max(0.0, 1.0 - valence_distance)
            score += valence_similarity * self.FEATURE_POINTS * user.valence_weight
        
        # Acousticness preference
        if user.likes_acoustic and user.acoustic_weight > 0:
            # Higher acousticness is better for acoustic-lovers
            score += song.acousticness * self.FEATURE_POINTS * user.acoustic_weight
        
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommend top-k songs for a user using the point-weighting strategy.
        
        Args:
            user: UserProfile with preferences
            k: Number of recommendations to return
            
        Returns:
            List of top-k Song objects sorted by score (highest first)
        """
        # Score all songs
        scored_songs = [
            (song, self.calculate_score(user, song))
            for song in self.songs
        ]
        
        # Sort by score descending, then by id for consistency
        scored_songs.sort(key=lambda x: (-x[1], x[0].id))
        
        # Return top-k songs
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Provide a detailed explanation of the recommendation score.
        """
        score = self.calculate_score(user, song)
        explanation_parts = [f"Score: {score:.2f}"]
        
        # Genre match (with fuzzy matching)
        genre_match, genre_type = self._fuzzy_match(user.favorite_genre, song.genre)
        if genre_match == 1.0:
            explanation_parts.append(f"✓ Genre exact: '{song.genre}' (+{self.GENRE_MATCH_POINTS:.1f})")
        elif genre_match == 0.5:
            explanation_parts.append(f"~ Genre fuzzy: '{song.genre}' → '{user.favorite_genre}' (+{self.GENRE_FUZZY_POINTS:.2f})")
        else:
            explanation_parts.append(f"✗ Genre: '{song.genre}' ≠ '{user.favorite_genre}'")
        
        # Mood match (with fuzzy matching)
        mood_match, mood_type = self._fuzzy_match(user.favorite_mood, song.mood)
        if mood_match == 1.0:
            explanation_parts.append(f"✓ Mood exact: '{song.mood}' (+{self.MOOD_MATCH_POINTS:.1f})")
        elif mood_match == 0.5:
            explanation_parts.append(f"~ Mood fuzzy: '{song.mood}' → '{user.favorite_mood}' (+{self.MOOD_FUZZY_POINTS:.2f})")
        else:
            explanation_parts.append(f"✗ Mood: '{song.mood}' ≠ '{user.favorite_mood}'")
        
        # Energy with tolerance
        energy_distance = abs(song.energy - user.target_energy)
        if energy_distance <= user.energy_tolerance:
            explanation_parts.append(
                f"✓ Energy: {song.energy:.2f} (within ±{user.energy_tolerance:.2f} of {user.target_energy:.2f})"
            )
        else:
            explanation_parts.append(
                f"~ Energy: {song.energy:.2f} (outside tolerance ±{user.energy_tolerance:.2f})"
            )
        
        # Extended features
        if user.target_danceability is not None and user.danceability_weight > 0:
            explanation_parts.append(f"Danceability: {song.danceability:.2f}")
        if user.target_valence is not None and user.valence_weight > 0:
            explanation_parts.append(f"Valence: {song.valence:.2f}")
        if user.likes_acoustic and user.acoustic_weight > 0:
            explanation_parts.append(f"Acousticness: {song.acousticness:.2f}")
        
        return " | ".join(explanation_parts)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    
    Args:
        csv_path: Path to the CSV file with song data
        
    Returns:
        List of dictionaries, each representing a song
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to appropriate types
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
        
        print(f"Successfully loaded {len(songs)} songs.")
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
    except Exception as e:
        print(f"Error loading songs: {e}")
    
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Enhanced functional recommendation with fuzzy matching, energy tolerance, and extended features.
    """
    # Constants with reduced genre dominance
    # ===== UPDATED WEIGHTS: Double Energy, Half Genre =====
    genre_match_points = 0.75      # Halved from 1.5
    genre_fuzzy_points = 0.375     # Halved from 0.75
    mood_match_points = 1.0        # Unchanged
    mood_fuzzy_points = 0.5        # Unchanged
    energy_max_points = 2.0        # Doubled from 1.0
    feature_points = 0.5           # Unchanged
    
    # Extract parameters with defaults
    energy_tolerance = user_prefs.get('energy_tolerance', 0.2)
    danceability_weight = user_prefs.get('danceability_weight', 0.0)
    valence_weight = user_prefs.get('valence_weight', 0.0)
    acoustic_weight = user_prefs.get('acoustic_weight', 0.0) if user_prefs.get('likes_acoustic') else 0.0
    
    scored_recommendations = []
    
    for song in songs:
        score = 0.0
        explanation_parts = []
        
        # Fuzzy genre matching
        user_genre = user_prefs['genre'].lower().strip()
        song_genre = song['genre'].lower().strip()
        genre_sim = SequenceMatcher(None, user_genre, song_genre).ratio()
        
        if user_genre == song_genre:
            score += genre_match_points
            explanation_parts.append(f"Genre:{song['genre']} (+{genre_match_points:.1f})")
        elif genre_sim >= 0.7:
            score += genre_fuzzy_points
            explanation_parts.append(f"Genre:{song['genre']}~{user_prefs['genre']} (+{genre_fuzzy_points:.2f})")
        else:
            explanation_parts.append(f"Genre:{song['genre']}")
        
        # Fuzzy mood matching
        user_mood = user_prefs['mood'].lower().strip()
        song_mood = song['mood'].lower().strip()
        mood_sim = SequenceMatcher(None, user_mood, song_mood).ratio()
        
        if user_mood == song_mood:
            score += mood_match_points
            explanation_parts.append(f"Mood:{song['mood']} (+{mood_match_points:.1f})")
        elif mood_sim >= 0.7:
            score += mood_fuzzy_points
            explanation_parts.append(f"Mood:{song['mood']}~{user_prefs['mood']} (+{mood_fuzzy_points:.2f})")
        else:
            explanation_parts.append(f"Mood:{song['mood']}")
        
        # Energy with tolerance
        energy_distance = abs(song['energy'] - user_prefs['energy'])
        if energy_distance <= energy_tolerance:
            energy_similarity = 1.0 - (energy_distance / energy_tolerance)
        else:
            excess_distance = energy_distance - energy_tolerance
            energy_similarity = max(0.0, 1.0 - excess_distance)
        energy_points = energy_similarity * energy_max_points
        score += energy_points
        explanation_parts.append(f"Energy:{song['energy']:.2f} (+{energy_points:.2f})")
        
        # Extended features: danceability
        if danceability_weight > 0:
            dance_distance = abs(song['danceability'] - user_prefs.get('target_danceability', 0.5))
            dance_sim = max(0.0, 1.0 - dance_distance)
            score += dance_sim * feature_points * danceability_weight
        
        # Extended features: valence
        if valence_weight > 0:
            valence_distance = abs(song['valence'] - user_prefs.get('target_valence', 0.5))
            valence_sim = max(0.0, 1.0 - valence_distance)
            score += valence_sim * feature_points * valence_weight
        
        # Extended features: acousticness
        if acoustic_weight > 0:
            score += song['acousticness'] * feature_points * acoustic_weight
        
        explanation = " | ".join(explanation_parts)
        scored_recommendations.append((song, score, explanation))
    
    # Sort by score descending, then by id for consistency
    scored_recommendations.sort(key=lambda x: (-x[1], x[0]['id']))
    
    # Return top-k recommendations
    return scored_recommendations[:k]
