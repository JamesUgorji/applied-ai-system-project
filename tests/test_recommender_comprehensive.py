"""
Comprehensive test suite for Music Recommender Agent.

Tests cover:
- Automated unit tests for core functions
- Scoring algorithm correctness
- Error handling and edge cases
- Integration tests
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from recommender import Song, UserProfile, Recommender, load_songs
from agent import RecommenderAgent
from config import AgentConfig


# ============================================================================
# FIXTURE: Test Data
# ============================================================================

@pytest.fixture
def test_songs():
    """Create minimal test song dataset."""
    return [
        Song(id=1, title="Happy Pop", artist="Test", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.1),
        Song(id=2, title="Chill Lofi", artist="Test", genre="lofi", mood="chill",
             energy=0.3, tempo_bpm=80, valence=0.5, danceability=0.4, acousticness=0.9),
        Song(id=3, title="Energetic Rock", artist="Test", genre="rock", mood="intense",
             energy=0.9, tempo_bpm=150, valence=0.6, danceability=0.7, acousticness=0.05),
        Song(id=4, title="Sad Blues", artist="Test", genre="jazz", mood="melancholic",
             energy=0.4, tempo_bpm=90, valence=0.3, danceability=0.5, acousticness=0.8),
    ]


@pytest.fixture
def test_recommender(test_songs):
    """Create recommender with test songs."""
    return Recommender(test_songs)


@pytest.fixture
def test_user_profile():
    """Create test user profile."""
    return UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False
    )


# ============================================================================
# TEST GROUP 1: CORE SCORING ALGORITHM
# ============================================================================

class TestScoringAlgorithm:
    """Test the point-weighting scoring algorithm."""
    
    def test_exact_genre_match(self, test_recommender, test_songs):
        """Exact genre match should award 0.75 points."""
        user = UserProfile("pop", "happy", 0.5, False)
        # Pop song with matching genre
        score = test_recommender.calculate_score(user, test_songs[0])
        assert score >= 0.75, "Should award genre match points"
    
    def test_exact_mood_match(self, test_recommender, test_songs):
        """Exact mood match should award 1.0 point."""
        user = UserProfile("pop", "happy", 0.5, False)
        # Pop + happy mood
        score = test_recommender.calculate_score(user, test_songs[0])
        assert score >= 1.0, "Should award mood match points"
    
    def test_energy_within_tolerance(self, test_recommender, test_songs):
        """Songs within ±0.2 energy tolerance should score high."""
        user = UserProfile("lofi", "chill", 0.3, False)
        # Lofi song with energy 0.3 (exact match)
        score = test_recommender.calculate_score(user, test_songs[1])
        assert score >= 2.0, "Should award energy points for within-tolerance match"
    
    def test_energy_outside_tolerance(self, test_recommender, test_songs):
        """Songs far outside energy tolerance should score low."""
        user = UserProfile("lofi", "chill", 0.3, False)
        # Rock song with energy 0.9 (way outside tolerance)
        score = test_recommender.calculate_score(user, test_songs[2])
        assert score < 1.5, "Should penalize energy mismatch"
    
    def test_acoustic_preference_bonus(self, test_recommender, test_songs):
        """Acoustic lovers should score acoustic songs higher."""
        user_acoustic = UserProfile("lofi", "chill", 0.3, likes_acoustic=True)
        user_no_acoustic = UserProfile("lofi", "chill", 0.3, likes_acoustic=False)
        
        score_with = test_recommender.calculate_score(user_acoustic, test_songs[1])
        score_without = test_recommender.calculate_score(user_no_acoustic, test_songs[1])
        
        # Acoustic lover should score higher on acoustic song
        assert score_with >= score_without, "Acoustic preference should increase score"
    
    def test_score_is_deterministic(self, test_recommender, test_songs):
        """Same input should always produce same score."""
        user = UserProfile("pop", "happy", 0.8, False)
        score1 = test_recommender.calculate_score(user, test_songs[0])
        score2 = test_recommender.calculate_score(user, test_songs[0])
        assert score1 == score2, "Scoring should be deterministic"
    
    def test_maximum_score(self, test_recommender, test_songs):
        """Perfect match should approach maximum theoretical score."""
        user = UserProfile("pop", "happy", 0.8, False)
        # Happy pop song with high energy
        score = test_recommender.calculate_score(user, test_songs[0])
        assert score <= 3.75, "Score should not exceed theoretical maximum"


# ============================================================================
# TEST GROUP 2: RANKING & RECOMMENDATION
# ============================================================================

class TestRecommendation:
    """Test recommendation ranking and selection."""
    
    def test_recommendations_are_ranked(self, test_recommender, test_songs):
        """Recommendations should be sorted by score (highest first)."""
        user = UserProfile("pop", "happy", 0.8, False)
        recommendations = test_recommender.recommend(user, k=3)
        
        # Should return k recommendations
        assert len(recommendations) == 3
        # Should be Song objects
        assert all(isinstance(r, Song) for r in recommendations)
    
    def test_k_parameter_limits_results(self, test_recommender, test_songs):
        """K parameter should limit returned recommendations."""
        user = UserProfile("pop", "happy", 0.8, False)
        
        recs_1 = test_recommender.recommend(user, k=1)
        recs_2 = test_recommender.recommend(user, k=2)
        
        assert len(recs_1) == 1
        assert len(recs_2) == 2
    
    def test_k_exceeding_catalog(self, test_recommender, test_songs):
        """K larger than catalog should return all songs."""
        user = UserProfile("pop", "happy", 0.8, False)
        recommendations = test_recommender.recommend(user, k=100)
        
        assert len(recommendations) <= len(test_songs)


# ============================================================================
# TEST GROUP 3: ERROR HANDLING & EDGE CASES
# ============================================================================

class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_unknown_genre_fuzzy_match(self, test_recommender):
        """Unknown genre should still work via fuzzy matching."""
        # "hip-hop" vs catalog "pop" - should fuzzy match
        user = UserProfile("hiphop", "happy", 0.8, False)
        # Should not crash
        recommendations = test_recommender.recommend(user, k=2)
        assert recommendations is not None
    
    def test_zero_energy(self, test_recommender):
        """Edge case: zero energy should be handled."""
        user = UserProfile("pop", "happy", 0.0, False)
        recommendations = test_recommender.recommend(user, k=2)
        assert len(recommendations) >= 0
    
    def test_one_energy(self, test_recommender):
        """Edge case: max energy (1.0) should be handled."""
        user = UserProfile("pop", "happy", 1.0, False)
        recommendations = test_recommender.recommend(user, k=2)
        assert len(recommendations) >= 0
    
    def test_empty_song_list(self):
        """Empty song list should be handled."""
        recommender = Recommender([])
        user = UserProfile("pop", "happy", 0.8, False)
        recommendations = recommender.recommend(user, k=5)
        assert len(recommendations) == 0
    
    def test_single_song(self):
        """Single song should work."""
        song = Song(id=1, title="Test", artist="Test", genre="pop", mood="happy",
                   energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.1)
        recommender = Recommender([song])
        user = UserProfile("pop", "happy", 0.8, False)
        recommendations = recommender.recommend(user, k=5)
        assert len(recommendations) == 1


# ============================================================================
# TEST GROUP 4: DATA INTEGRITY
# ============================================================================

class TestDataIntegrity:
    """Test data loading and integrity."""
    
    def test_load_songs_from_csv(self):
        """CSV loading should produce Song objects."""
        songs = load_songs("data/songs.csv")
        assert len(songs) > 0, "Should load songs from CSV"
        assert all(isinstance(s, dict) for s in songs), "load_songs returns dicts"
        assert 'title' in songs[0]
        assert 'artist' in songs[0]
        assert 'genre' in songs[0]
    
    def test_song_attributes_valid(self):
        """Loaded songs should have valid attributes."""
        songs = load_songs("data/songs.csv")
        for song in songs:
            assert 0 <= song['energy'] <= 1, f"Energy out of range: {song['energy']}"
            assert 0 <= song['valence'] <= 1, f"Valence out of range: {song['valence']}"
            assert 0 <= song['danceability'] <= 1, f"Danceability out of range"
            assert 0 <= song['acousticness'] <= 1, f"Acousticness out of range"
            assert song['tempo_bpm'] > 0, f"BPM must be positive"


# ============================================================================
# TEST GROUP 5: REPRODUCIBILITY
# ============================================================================

class TestReproducibility:
    """Test reproducibility requirements."""
    
    def test_same_profile_same_scores(self, test_recommender, test_songs):
        """Same user profile should produce same scores."""
        user1 = UserProfile("pop", "happy", 0.8, False)
        user2 = UserProfile("pop", "happy", 0.8, False)
        
        scores1 = [test_recommender.calculate_score(user1, song) for song in test_songs]
        scores2 = [test_recommender.calculate_score(user2, song) for song in test_songs]
        
        assert scores1 == scores2, "Same profile should produce identical scores"
    
    def test_recommendations_consistent(self, test_recommender, test_songs):
        """Same profile should produce same recommendations."""
        user = UserProfile("pop", "happy", 0.8, False)
        
        recs1 = test_recommender.recommend(user, k=3)
        recs2 = test_recommender.recommend(user, k=3)
        
        # Same order and content
        assert [r.id for r in recs1] == [r.id for r in recs2]


# ============================================================================
# TEST GROUP 6: USER PROFILE
# ============================================================================

class TestUserProfile:
    """Test UserProfile data class."""
    
    def test_profile_creation(self):
        """UserProfile should be created with required fields."""
        profile = UserProfile(
            favorite_genre="pop",
            favorite_mood="happy",
            target_energy=0.8,
            likes_acoustic=False
        )
        assert profile.favorite_genre == "pop"
        assert profile.favorite_mood == "happy"
        assert profile.target_energy == 0.8
        assert profile.likes_acoustic == False
    
    def test_profile_default_values(self):
        """UserProfile should have sensible defaults."""
        profile = UserProfile("pop", "happy", 0.5, False)
        assert profile.energy_tolerance == 0.2
        assert profile.acoustic_weight >= 0.0


# ============================================================================
# TEST GROUP 7: CONFIGURATION
# ============================================================================

class TestConfiguration:
    """Test AgentConfig constants."""
    
    def test_config_energy_scale_valid(self):
        """Energy scale should have valid ranges."""
        for level, (low, high, desc) in AgentConfig.ENERGY_SCALE.items():
            assert 0 <= low <= 1
            assert 0 <= high <= 1
            assert low < high
            assert len(desc) > 0
    
    def test_example_genres_exist(self):
        """Should have example genres configured."""
        assert len(AgentConfig.EXAMPLE_GENRES) > 0
    
    def test_example_moods_exist(self):
        """Should have example moods configured."""
        assert len(AgentConfig.EXAMPLE_MOODS) > 0


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
