"""
Demonstration of the point-weighting recommendation strategy.

Shows how scores are calculated using:
- +2.0 points for genre match
- +1.0 point for mood match  
- Up to +1.0 point for energy similarity
"""

from src.recommender import load_songs, recommend_songs

def demo_weighting_strategy():
    """Demo showing the point-weighting strategy in action"""
    
    print("=" * 80)
    print("MUSIC RECOMMENDER - POINT-WEIGHTING STRATEGY DEMO")
    print("=" * 80)
    
    # Load songs from CSV
    songs = load_songs("data/songs.csv")
    
    if not songs:
        print("No songs loaded. Exiting.")
        return
    
    # Example 1: Lo-fi focused listener
    print("\n" + "-" * 80)
    print("PROFILE 1: Lo-fi Focused Listener")
    print("-" * 80)
    
    profile_1 = {"genre": "lofi", "mood": "focused", "energy": 0.40}
    print(f"Preferences: {profile_1}")
    print("\nWeighting Strategy:")
    print("  • Genre match (lofi):     +2.0 points")
    print("  • Mood match (focused):   +1.0 point")
    print("  • Energy similarity:      up to +1.0 point (based on distance from 0.40)")
    
    recommendations_1 = recommend_songs(profile_1, songs, k=5)
    
    print(f"\nTop {len(recommendations_1)} Recommendations:")
    for i, (song, score, explanation) in enumerate(recommendations_1, 1):
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   {explanation}")
    
    # Example 2: Pop happy listener
    print("\n" + "-" * 80)
    print("PROFILE 2: Pop Happy Listener")
    print("-" * 80)
    
    profile_2 = {"genre": "pop", "mood": "happy", "energy": 0.80}
    print(f"Preferences: {profile_2}")
    
    recommendations_2 = recommend_songs(profile_2, songs, k=5)
    
    print(f"\nTop {len(recommendations_2)} Recommendations:")
    for i, (song, score, explanation) in enumerate(recommendations_2, 1):
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   {explanation}")
    
    # Example 3: Rock intense listener
    print("\n" + "-" * 80)
    print("PROFILE 3: Rock Intense Listener")
    print("-" * 80)
    
    profile_3 = {"genre": "rock", "mood": "intense", "energy": 0.90}
    print(f"Preferences: {profile_3}")
    
    recommendations_3 = recommend_songs(profile_3, songs, k=5)
    
    print(f"\nTop {len(recommendations_3)} Recommendations:")
    for i, (song, score, explanation) in enumerate(recommendations_3, 1):
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   {explanation}")
    
    print("\n" + "=" * 80)
    print("SCORING NOTES:")
    print("=" * 80)
    print("• Maximum possible score: 4.0 (2.0 genre + 1.0 mood + 1.0 energy)")
    print("• Genre & mood are binary (match or no match)")
    print("• Energy similarity scales linearly with distance:")
    print("    Score = max(0, 1.0 - |song_energy - target_energy|)")
    print("• Songs are ranked by total score (highest first)")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    demo_weighting_strategy()
