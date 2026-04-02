"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

def main() -> None:
    songs = load_songs("data/songs.csv") 

    # User preference profile using the point-weighting strategy
    # Genre: +2.0 points, Mood: +1.0 point, Energy: up to +1.0 point
    user_prefs = {
        "genre": "lofi",
        "mood": "focused",
        "energy": 0.40
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # Structure: (song_dict, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
