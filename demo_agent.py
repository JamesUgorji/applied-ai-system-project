"""
Demo script for the Music Recommender Agent.

This script simulates user interaction with the agent to showcase the workflow.
Run this to see the agent in action without manually entering preferences.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from recommender import load_songs, Recommender, Song, UserProfile
from config import setup_logging, AgentConfig, save_session_data

def demo_workflow():
    """Run a demo workflow showing the agent's capabilities."""
    
    logger, run_id = setup_logging()
    
    print("\n" + "=" * 60)
    print("🎵 Music Recommender Agent - Interactive Demo")
    print("=" * 60)
    
    logger.info("Starting demo workflow")
    
    # Load songs
    print("\n📚 Loading songs from catalog...")
    songs_dicts = load_songs("data/songs.csv")
    # Convert dictionaries to Song objects for the Recommender class
    songs = [Song(**song_dict) for song_dict in songs_dicts]
    recommender = Recommender(songs)
    print(f"✅ Loaded {len(songs)} songs")
    logger.info(f"Loaded {len(songs)} songs")
    
    # Create a demo user profile
    print("\n" + "-" * 60)
    print("👤 Demo User Profile")
    print("-" * 60)
    user_profile = UserProfile(
        favorite_genre="lofi",
        favorite_mood="focused",
        target_energy=0.4,
        likes_acoustic=True
    )
    print(f"Genre: {user_profile.favorite_genre}")
    print(f"Mood: {user_profile.favorite_mood}")
    print(f"Energy: {user_profile.target_energy}")
    print(f"Likes Acoustic: {user_profile.likes_acoustic}")
    logger.info(f"Created user profile: {user_profile}")
    
    # Generate recommendations
    print("\n" + "-" * 60)
    print("🔍 Generating Initial Recommendations")
    print("-" * 60)
    
    scored_songs = []
    for song in songs:
        score = recommender.calculate_score(user_profile, song)
        scored_songs.append((song, score))
    
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    top_songs = scored_songs[:5]
    
    recommendations = []
    for i, (song, score) in enumerate(top_songs, 1):
        confidence = recommender.calculate_confidence(user_profile, song)
        confidence_bar = "🟢" if confidence >= 0.7 else "🟡" if confidence >= 0.5 else "🔴"
        recommendations.append((song.__dict__, score, f"Matches your {user_profile.favorite_genre} preference"))
        print(f"\n{i}. 🎵 {song.title} by {song.artist}")
        print(f"   Genre: {song.genre} | Mood: {song.mood} | Energy: {song.energy:.2f}")
        print(f"   Score: {score:.2f} | Confidence: {confidence_bar} {confidence*100:.0f}%")
    
    logger.info(f"Generated {len(recommendations)} recommendations")
    
    # Demonstrate refinement
    print("\n" + "-" * 60)
    print("💬 Demonstrating Preference Adjustment")
    print("-" * 60)
    print("\nOriginal energy preference: 0.40")
    print("Adjusting to: more energetic (0.50)...")
    
    user_profile.target_energy = 0.50
    logger.info(f"Adjusted energy to {user_profile.target_energy}")
    
    print("\n🔄 Re-generating recommendations with new preference...")
    scored_songs = []
    for song in songs:
        score = recommender.calculate_score(user_profile, song)
        scored_songs.append((song, score))
    
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    top_songs = scored_songs[:5]
    
    recommendations = []
    for i, (song, score) in enumerate(top_songs, 1):
        confidence = recommender.calculate_confidence(user_profile, song)
        confidence_bar = "🟢" if confidence >= 0.7 else "🟡" if confidence >= 0.5 else "🔴"
        recommendations.append((song.__dict__, score, f"Matches adjusted {user_profile.favorite_mood} mood"))
        print(f"\n{i}. 🎵 {song.title} by {song.artist}")
        print(f"   Genre: {song.genre} | Mood: {song.mood} | Energy: {song.energy:.2f}")
        print(f"   Score: {score:.2f} | Confidence: {confidence_bar} {confidence*100:.0f}%")
    
    # Save session
    print("\n" + "-" * 60)
    print("💾 Saving Session Data")
    print("-" * 60)
    
    session_file = save_session_data(run_id, user_profile.__dict__, recommendations, logger)
    print(f"\n✅ Session saved to: {session_file}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Demo Complete!")
    print("=" * 60)
    print(f"\nRun ID: {run_id}")
    print(f"Songs processed: {len(songs)}")
    print(f"Recommendations generated: {len(recommendations)}")
    print(f"Log file: logs/agent_run_{run_id}.log")
    print(f"Session data: {session_file}")
    
    print("\n💡 To run the interactive version:")
    print("   python -m src.agent")
    
    logger.info("Demo workflow completed successfully")


if __name__ == "__main__":
    demo_workflow()
