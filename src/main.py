"""
Command line runner for the Music Recommender Simulation.

This file provides a menu to choose between:
1. Basic recommender (non-interactive)
2. Interactive agent (conversational)
3. Demo of agent workflow
"""

from recommender import load_songs, recommend_songs

def show_menu() -> str:
    """Display main menu and get user choice."""
    print("\n🎵 Music Recommender System")
    print("=" * 50)
    print("\nChoose a mode:")
    print("  1. Basic Recommender (non-interactive)")
    print("  2. Interactive Agent (conversational)")
    print("  3. Agent Demo (simulated workflow)")
    print("  4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def run_basic_recommender() -> None:
    """Run the non-interactive basic recommender."""
    print("\n" + "=" * 50)
    print("📊 Basic Recommender")
    print("=" * 50)
    
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

def run_interactive_agent() -> None:
    """Run the interactive recommendation agent."""
    from agent import RecommenderAgent
    
    agent = RecommenderAgent()
    agent.run()

def run_agent_demo() -> None:
    """Run a demo of the agent workflow."""
    # Import the demo module dynamically to avoid circular imports
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "demo_agent.py"], cwd=".")
    sys.exit(result.returncode)

def main() -> None:
    """Main entry point with menu."""
    choice = show_menu()
    
    if choice == '1':
        run_basic_recommender()
    elif choice == '2':
        run_interactive_agent()
    elif choice == '3':
        run_agent_demo()
    elif choice == '4':
        print("\n👋 Goodbye!")
        return
    
    # Show menu again after completion
    main()


if __name__ == "__main__":
    main()
