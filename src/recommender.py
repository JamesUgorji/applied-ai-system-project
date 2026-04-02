from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    # Point-weighting strategy
    GENRE_MATCH_POINTS = 2.0
    MOOD_MATCH_POINTS = 1.0
    ENERGY_MAX_POINTS = 1.0

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def calculate_score(self, user: UserProfile, song: Song) -> float:
        """
        Calculate a recommendation score using point-weighting strategy:
        - +2.0 points for genre match
        - +1.0 point for mood match
        - Up to +1.0 point for energy similarity (based on distance from target)
        
        Args:
            user: UserProfile with preferences
            song: Song to score
            
        Returns:
            Total score as a float
        """
        score = 0.0
        
        # Genre match: +2.0 points
        if song.genre.lower() == user.favorite_genre.lower():
            score += self.GENRE_MATCH_POINTS
        
        # Mood match: +1.0 point
        if song.mood.lower() == user.favorite_mood.lower():
            score += self.MOOD_MATCH_POINTS
        
        # Energy similarity: up to +1.0 point
        # Linear decay based on euclidean distance from target energy
        energy_distance = abs(song.energy - user.target_energy)
        # Clamp distance to [0, 1] range for scoring
        energy_similarity = max(0.0, 1.0 - energy_distance)
        score += energy_similarity * self.ENERGY_MAX_POINTS
        
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
        Provide a human-readable explanation of why a song was recommended.
        
        Args:
            user: UserProfile with preferences
            song: Song being explained
            
        Returns:
            String explaining the recommendation score breakdown
        """
        score = self.calculate_score(user, song)
        explanation_parts = [f"Score: {score:.2f}"]
        
        # Genre match
        genre_match = song.genre.lower() == user.favorite_genre.lower()
        if genre_match:
            explanation_parts.append(f"✓ Genre match: '{song.genre}' (+{self.GENRE_MATCH_POINTS:.1f})")
        else:
            explanation_parts.append(f"✗ Genre: '{song.genre}' (not '{user.favorite_genre}')")
        
        # Mood match
        mood_match = song.mood.lower() == user.favorite_mood.lower()
        if mood_match:
            explanation_parts.append(f"✓ Mood match: '{song.mood}' (+{self.MOOD_MATCH_POINTS:.1f})")
        else:
            explanation_parts.append(f"✗ Mood: '{song.mood}' (not '{user.favorite_mood}')")
        
        # Energy similarity
        energy_distance = abs(song.energy - user.target_energy)
        energy_similarity = max(0.0, 1.0 - energy_distance)
        energy_points = energy_similarity * self.ENERGY_MAX_POINTS
        explanation_parts.append(
            f"Energy: {song.energy:.2f} vs {user.target_energy:.2f} "
            f"(distance: {energy_distance:.2f}, +{energy_points:.2f})"
        )
        
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


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic using point-weighting strategy.
    
    Scoring:
    - +2.0 points for genre match
    - +1.0 point for mood match
    - Up to +1.0 point for energy similarity
    
    Args:
        user_prefs: Dictionary with keys 'genre', 'mood', 'energy'
        songs: List of song dictionaries
        k: Number of recommendations to return
        
    Returns:
        List of tuples: (song_dict, score, explanation)
        Sorted by score in descending order
    """
    genre_match_points = 2.0
    mood_match_points = 1.0
    energy_max_points = 1.0
    
    scored_recommendations = []
    
    for song in songs:
        score = 0.0
        explanation_parts = []
        
        # Genre match: +2.0 points
        if song['genre'].lower() == user_prefs['genre'].lower():
            score += genre_match_points
            explanation_parts.append(f"Genre:{song['genre']} (+{genre_match_points:.1f})")
        else:
            explanation_parts.append(f"Genre:{song['genre']} (not {user_prefs['genre']})")
        
        # Mood match: +1.0 point
        if song['mood'].lower() == user_prefs['mood'].lower():
            score += mood_match_points
            explanation_parts.append(f"Mood:{song['mood']} (+{mood_match_points:.1f})")
        else:
            explanation_parts.append(f"Mood:{song['mood']} (not {user_prefs['mood']})")
        
        # Energy similarity: up to +1.0 point
        energy_distance = abs(song['energy'] - user_prefs['energy'])
        energy_similarity = max(0.0, 1.0 - energy_distance)
        energy_points = energy_similarity * energy_max_points
        score += energy_points
        explanation_parts.append(
            f"Energy:{song['energy']:.2f} vs {user_prefs['energy']:.2f} (+{energy_points:.2f})"
        )
        
        explanation = " | ".join(explanation_parts)
        scored_recommendations.append((song, score, explanation))
    
    # Sort by score descending, then by id for consistency
    scored_recommendations.sort(key=lambda x: (-x[1], x[0]['id']))
    
    # Return top-k recommendations
    return scored_recommendations[:k]
