"""
Interactive Music Recommender Agent.

This agent converses with users to understand their music preferences,
generates personalized recommendations, and refines them based on feedback.

Workflow:
  1. User Profiling: Gather preferences through questions
  2. Generate: Create initial recommendations with explanations
  3. Refine: Accept feedback and adjust recommendations
  4. Export: Save results and session data
"""

import logging
from typing import Optional, List, Tuple
from recommender import load_songs, Recommender, Song, UserProfile
from config import setup_logging, AgentConfig, save_session_data

# Initialize logging
logger, run_id = setup_logging()


class RecommenderAgent:
    """
    Interactive agent for music recommendations.
    Handles user profiling, recommendations, and refinement loops.
    """
    
    def __init__(self, songs_path: str = "data/songs.csv"):
        """
        Initialize the agent with songs data.
        
        Args:
            songs_path: Path to the songs CSV file
        """
        try:
            songs_dicts = load_songs(songs_path)
            # Convert dictionaries to Song objects for the Recommender class
            self.songs = [Song(**song_dict) for song_dict in songs_dicts]
            self.recommender = Recommender(self.songs)
            self.user_profile: Optional[UserProfile] = None
            self.current_recommendations: List[Tuple] = []
            
            logger.info(f"Agent initialized with {len(self.songs)} songs")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise
    
    def run(self) -> None:
        """Main agent workflow."""
        logger.info("Starting interactive recommendation workflow")
        print("\n🎵 Welcome to the Music Recommender Agent!")
        print("=" * 50)
        
        try:
            # Phase 1: User Profiling
            self.user_profile = self._profile_user()
            logger.info(f"User profile created: {self.user_profile}")
            
            # Phase 2: Generate Recommendations
            self._generate_recommendations()
            
            # Phase 3: Refinement Loop
            self._refinement_loop()
            
            # Phase 4: Export Results
            self._export_results()
            
            print("\n✅ Workflow complete!")
            logger.info("Agent workflow completed successfully")
            
        except KeyboardInterrupt:
            logger.info("Workflow interrupted by user")
            print("\n\n👋 Workflow cancelled.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")
            raise
    
    # ============================================================================
    # PHASE 1: USER PROFILING
    # ============================================================================
    
    def _profile_user(self) -> UserProfile:
        """
        Conversational phase to build user preference profile.
        
        Returns:
            UserProfile: User's preferences
        """
        print("\n📋 Let's learn about your music taste!")
        print("-" * 50)
        
        # Gather genre
        genre = self._get_genre_preference()
        logger.info(f"User selected genre: {genre}")
        
        # Gather mood
        mood = self._get_mood_preference()
        logger.info(f"User selected mood: {mood}")
        
        # Gather energy level
        energy = self._get_energy_preference()
        logger.info(f"User selected energy: {energy}")
        
        # Gather acoustic preference
        likes_acoustic = self._get_acoustic_preference()
        logger.info(f"User likes acoustic: {likes_acoustic}")
        
        # Create profile
        profile = UserProfile(
            favorite_genre=genre,
            favorite_mood=mood,
            target_energy=energy,
            likes_acoustic=likes_acoustic
        )
        
        return profile
    
    def _get_genre_preference(self) -> str:
        """Prompt user for favorite genre."""
        print(f"\n🎸 Genres in our catalog: {', '.join(AgentConfig.EXAMPLE_GENRES)}")
        while True:
            genre = input("What's your favorite genre? ").strip()
            if genre:
                return genre
            print("Please enter a genre.")
    
    def _get_mood_preference(self) -> str:
        """Prompt user for favorite mood."""
        print(f"\n😊 Moods available: {', '.join(AgentConfig.EXAMPLE_MOODS)}")
        while True:
            mood = input("What mood are you in? ").strip()
            if mood:
                return mood
            print("Please enter a mood.")
    
    def _get_energy_preference(self) -> float:
        """Prompt user for energy level on a scale."""
        print("\n⚡ Energy Level Scale:")
        for level, (low, high, desc) in AgentConfig.ENERGY_SCALE.items():
            print(f"  {level.capitalize()}: {low}-{high} ({desc})")
        
        while True:
            try:
                energy_input = input("Enter energy level (0-1) or (low/medium/high): ").strip().lower()
                
                if energy_input in AgentConfig.ENERGY_SCALE:
                    low, high, _ = AgentConfig.ENERGY_SCALE[energy_input]
                    energy = (low + high) / 2  # Use midpoint
                    return energy
                else:
                    energy = float(energy_input)
                    if 0 <= energy <= 1:
                        return energy
                    print("Please enter a value between 0 and 1.")
            except ValueError:
                print("Invalid input. Enter a number (0-1) or (low/medium/high).")
    
    def _get_acoustic_preference(self) -> bool:
        """Prompt user if they like acoustic music."""
        while True:
            response = input("\n🎶 Do you like acoustic music? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            print("Please answer 'yes' or 'no'.")
    
    # ============================================================================
    # PHASE 2: GENERATE RECOMMENDATIONS
    # ============================================================================
    
    def _generate_recommendations(self, k: int = AgentConfig.DEFAULT_K_RECOMMENDATIONS) -> None:
        """
        Generate personalized recommendations.
        
        Args:
            k: Number of recommendations to generate
        """
        logger.info(f"Generating {k} recommendations for user")
        
        print(f"\n🔍 Finding your top {k} recommendations...")
        print("-" * 50)
        
        # Score all songs
        scored_songs = []
        for song in self.songs:
            score = self.recommender.calculate_score(self.user_profile, song)
            scored_songs.append((song, score))
        
        # Sort and get top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        top_songs = scored_songs[:k]
        
        # Generate explanations with confidence
        self.current_recommendations = []
        for i, (song, score) in enumerate(top_songs, 1):
            explanation = self._explain_recommendation(song)
            confidence = self._get_confidence(song)
            self.current_recommendations.append((song.__dict__, score, explanation))
            
            # Confidence indicator
            confidence_bar = "🟢" if confidence >= 0.7 else "🟡" if confidence >= 0.5 else "🔴"
            
            print(f"\n{i}. 🎵 {song.title} by {song.artist}")
            print(f"   Score: {score:.2f} | Confidence: {confidence_bar} {confidence*100:.0f}%")
            print(f"   ➜ {explanation}")
        
        logger.info(f"Generated {len(self.current_recommendations)} recommendations")
    
    def _explain_recommendation(self, song: Song) -> str:
        """
        Generate a human-readable explanation for why a song was recommended.
        
        Args:
            song: The song to explain
        
        Returns:
            str: Explanation
        """
        matches = []
        
        # Check genre match
        if self.user_profile.favorite_genre.lower() in song.genre.lower() or \
           song.genre.lower() in self.user_profile.favorite_genre.lower():
            matches.append(f"matches your {self.user_profile.favorite_genre} preference")
        
        # Check mood match
        if self.user_profile.favorite_mood.lower() in song.mood.lower() or \
           song.mood.lower() in self.user_profile.favorite_mood.lower():
            matches.append(f"has that {self.user_profile.favorite_mood} vibe")
        
        # Check energy
        energy_diff = abs(song.energy - self.user_profile.target_energy)
        if energy_diff < 0.2:
            matches.append(f"has your target energy level ({song.energy:.1f})")
        
        # Check acoustic
        if self.user_profile.likes_acoustic and song.acousticness > 0.6:
            matches.append("features acoustic elements")
        
        if matches:
            return " and ".join(matches)
        return "offers an interesting combination of features"
    
    def _get_confidence(self, song: Song) -> float:
        """
        Get confidence score for a recommendation.
        
        Args:
            song: Song to evaluate
        
        Returns:
            float: Confidence 0-1
        """
        return self.recommender.calculate_confidence(self.user_profile, song)
    
    # ============================================================================
    # PHASE 3: REFINEMENT LOOP
    # ============================================================================
    
    def _refinement_loop(self) -> None:
        """
        Interactive refinement loop: user can provide feedback and adjust preferences.
        """
        logger.info("Starting refinement loop")
        
        print("\n" + "=" * 50)
        print("💬 Refinement Mode")
        print("=" * 50)
        print("\nYou can:")
        print("  - Type 'more <feature>' to adjust (e.g., 'more energetic')")
        print("  - Type 'less <feature>' to adjust")
        print("  - Type 'list' to see current recommendations again")
        print("  - Type 'done' to finish")
        
        while True:
            user_input = input("\n> ").strip().lower()
            
            if user_input == 'done':
                logger.info("User finished refinement")
                break
            elif user_input == 'list':
                self._show_recommendations()
            elif user_input.startswith('more '):
                feature = user_input[5:].strip()
                self._adjust_preference(feature, direction='more')
                self._generate_recommendations()
            elif user_input.startswith('less '):
                feature = user_input[5:].strip()
                self._adjust_preference(feature, direction='less')
                self._generate_recommendations()
            elif user_input:
                print("Commands: 'more <feature>', 'less <feature>', 'list', or 'done'")
    
    def _adjust_preference(self, feature: str, direction: str) -> None:
        """
        Adjust user preference based on feedback.
        
        Args:
            feature: Feature to adjust (energy, acoustic, etc.)
            direction: 'more' or 'less'
        """
        adjustment = AgentConfig.WEIGHT_ADJUSTMENT
        if direction == 'less':
            adjustment = -adjustment
        
        feature_lower = feature.lower()
        
        if 'energy' in feature_lower:
            self.user_profile.target_energy = max(0, min(1, self.user_profile.target_energy + adjustment))
            logger.info(f"Adjusted energy to {self.user_profile.target_energy:.2f}")
            print(f"✅ Energy adjusted to {self.user_profile.target_energy:.2f}")
        elif 'acoustic' in feature_lower:
            self.user_profile.likes_acoustic = (direction == 'more')
            logger.info(f"Acoustic preference set to {self.user_profile.likes_acoustic}")
            print(f"✅ Acoustic preference updated")
        else:
            print(f"I don't know how to adjust '{feature}'. Try 'energy' or 'acoustic'.")
            logger.warning(f"Unknown adjustment requested: {feature}")
    
    def _show_recommendations(self) -> None:
        """Display current recommendations."""
        if not self.current_recommendations:
            print("No recommendations yet.")
            return
        
        print("\n" + "=" * 50)
        print("📊 Current Recommendations")
        print("=" * 50)
        
        for i, (song_dict, score, explanation) in enumerate(self.current_recommendations, 1):
            print(f"\n{i}. 🎵 {song_dict['title']} by {song_dict['artist']}")
            print(f"   Score: {score:.2f}")
            print(f"   ➜ {explanation}")
    
    # ============================================================================
    # PHASE 4: EXPORT RESULTS
    # ============================================================================
    
    def _export_results(self) -> None:
        """Export final session data and results."""
        logger.info("Exporting results")
        
        print("\n" + "=" * 50)
        print("💾 Saving Your Session")
        print("=" * 50)
        
        # Save to JSON
        session_file = save_session_data(
            run_id,
            self.user_profile.__dict__,
            self.current_recommendations,
            logger
        )
        
        print(f"\n✅ Results saved to: {session_file}")
        
        # Show summary
        print("\n📈 Session Summary")
        print("-" * 50)
        print(f"Run ID: {run_id}")
        print(f"Preferences: {self.user_profile.favorite_genre} ({self.user_profile.favorite_mood}, energy: {self.user_profile.target_energy:.1f})")
        print(f"Recommendations generated: {len(self.current_recommendations)}")
        print(f"\nDetailed logs saved to: logs/agent_run_{run_id}.log")


def main() -> None:
    """Entry point for the agent."""
    agent = RecommenderAgent()
    agent.run()


if __name__ == "__main__":
    main()
