# 🎵 Interactive Music Recommender Agent

## Overview

The Interactive Recommender Agent is an agentic workflow that converses with users to understand their music preferences, generates personalized song recommendations, and iteratively refines results based on feedback.

### Key Features

✅ **Reproducible & Logged**: Every run is tracked with unique IDs, detailed logs, and session data saved as JSON  
✅ **Error Handling & Guardrails**: Graceful error recovery and validation of user inputs  
✅ **Clear Setup**: Single script to set up everything needed to run  
✅ **Interactive**: Conversational approach to gather preferences and refine recommendations  
✅ **Transparent Explanations**: Every recommendation includes a reason why it matched user preferences  

---

## Quick Start

### 1. Setup (One-time)

```bash
# Make setup script executable (if needed)
chmod +x setup.sh

# Run setup
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Provide next steps

### 2. Run the Interactive Agent

```bash
# Activate virtual environment (if not already activated)
source .venv/bin/activate

# Run the interactive agent
python -m src.agent
```

### 3. View Results

Each session generates:
- **Log file**: `logs/agent_run_TIMESTAMP.log` - detailed execution trace
- **Session data**: `logs/session_TIMESTAMP.json` - user profile and recommendations in JSON format

---

## Workflow Phases

### Phase 1: User Profiling (Conversational)

The agent asks questions to understand your music taste:

```
🎸 Genres in our catalog: lofi, pop, rock, ambient, jazz, synthwave, indie pop, electronic
What's your favorite genre? lofi

😊 Moods available: chill, focused, happy, intense, relaxed, moody, joyful
What mood are you in? focused

⚡ Energy Level Scale:
  Low: 0-0.3 (Chill, background music)
  Medium: 0.3-0.65 (Balanced energy)
  High: 0.65-1.0 (Energetic, intense)
Enter energy level (0-1) or (low/medium/high): 0.4

🎶 Do you like acoustic music? (yes/no): yes
```

**What gets captured:**
- Favorite genre (with fuzzy matching support)
- Preferred mood
- Target energy level (0-1 scale)
- Acoustic music preference

### Phase 2: Generate Recommendations

The agent scores all 20 songs against your profile using:
- **Genre matching** (0.75 points) - exact or fuzzy match
- **Mood matching** (1.0 points) - exact or fuzzy match  
- **Energy alignment** (2.0 points max) - based on tolerance of ±0.2
- **Acoustic preference** (0.5 points) - if you like acoustic music

**Output example:**
```
1. 🎵 Focus Flow by LoRoom
   Score: 3.75
   ➜ matches your lofi preference and has that focused vibe
```

### Phase 3: Refinement Loop

Iteratively improve recommendations by providing feedback:

```
💬 Refinement Mode
========================================

You can:
  - Type 'more <feature>' to adjust (e.g., 'more energetic')
  - Type 'less <feature>' to adjust
  - Type 'list' to see current recommendations again
  - Type 'done' to finish

> more energetic
✅ Energy adjusted to 0.50

🔄 Re-generating with new preference...
```

Supported adjustments:
- `more energetic` / `less energetic` - adjusts energy by ±0.1
- `more acoustic` / `less acoustic` - toggles acoustic preference

### Phase 4: Export & Save

Session data automatically saved including:
- User profile (preferences and settings)
- Final recommendations with scores and explanations
- Full execution log

---

## Running Different Modes

### Interactive Agent
```bash
python -m src.agent
```
Conversational interface with full workflow

### Demo (Non-interactive)
```bash
python3 demo_agent.py
```
Watch a simulated workflow with pre-set preferences

### Basic Recommender (Legacy)
```bash
python -m src.main
# Then select option 1
```
Simple non-interactive recommendations

### Menu Interface
```bash
python -m src.main
# Choose from options 1-4
```

---

## Understanding the Logs

### Log File Format (`logs/agent_run_*.log`)

```
2026-05-02 22:17:14,123 - recommender_agent - INFO - Agent initialized with 20 songs
2026-05-02 22:17:14,124 - recommender_agent - INFO - User profile created: UserProfile(...)
2026-05-02 22:17:15,456 - recommender_agent - INFO - Generated 5 recommendations
2026-05-02 22:17:20,789 - recommender_agent - INFO - Adjusted energy to 0.50
2026-05-02 22:17:22,001 - recommender_agent - INFO - Session data saved to logs/session_*.json
```

Log levels:
- **INFO**: Key workflow steps
- **DEBUG**: Detailed execution information
- **ERROR**: Problems and failures
- **WARNING**: Unexpected but recoverable situations

### Session Data (`logs/session_*.json`)

```json
{
  "run_id": "20260502_221903",
  "timestamp": "2026-05-02T22:19:03.456789",
  "user_profile": {
    "favorite_genre": "lofi",
    "favorite_mood": "focused",
    "target_energy": 0.4,
    "likes_acoustic": true
  },
  "recommendations": [
    {
      "title": "Focus Flow",
      "artist": "LoRoom",
      "score": 3.75,
      "explanation": "matches your lofi preference and has that focused vibe"
    }
  ]
}
```

---

## Architecture

### Core Components

#### `src/agent.py` - RecommenderAgent Class
- **_profile_user()**: Conversational phase to build preference profile
- **_generate_recommendations()**: Scores and ranks songs
- **_refinement_loop()**: Interactive feedback and adjustment loop
- **_export_results()**: Saves session data

#### `src/config.py` - Configuration & Logging
- **setup_logging()**: Initialize centralized logging
- **AgentConfig**: Constants for energy scales, genres, moods
- **save_session_data()**: Persist results to JSON

#### `src/recommender.py` - Scoring Engine
- **Recommender.calculate_score()**: Point-weighting algorithm
- **Song**: Dataclass representing a song with features
- **UserProfile**: Dataclass for user preferences

### Data Flow

```
User Input
    ↓
Profile Creation (Phase 1)
    ↓
Load Songs + Recommender
    ↓
Score All Songs (Phase 2)
    ↓
Sort by Score + Show Top-K
    ↓
Refinement Loop (Phase 3)
    ├─ User Feedback
    ├─ Adjust Profile
    └─ Re-score
    ↓
Save Session (Phase 4)
    ├─ Logs
    └─ JSON Export
```

---

## Scoring Algorithm

The agent uses a **point-weighting strategy** inspired by real recommendation systems:

| Feature | Points | How It Works |
|---------|--------|--------------|
| Genre Match (exact) | 0.75 | User's genre matches song's genre exactly |
| Genre Match (fuzzy) | 0.375 | Similar genre names (similarity > 0.7) |
| Mood Match (exact) | 1.0 | User's mood matches song's mood exactly |
| Mood Match (fuzzy) | 0.5 | Similar mood names |
| Energy Alignment | 2.0 max | Distance from user's target energy |
| Acoustic | 0.5 max | Acousticness value (if user likes acoustic) |
| **Maximum Total** | **3.75** | Theoretical max for perfect match |

**Energy Tolerance**: ±0.2 around target (e.g., if target is 0.4, songs 0.2-0.6 get full points)

---

## Extending the Agent

### Add New Preference Dimensions

1. Add field to `UserProfile` in `recommender.py`:
```python
@dataclass
class UserProfile:
    target_tempo: Optional[float] = None
    tempo_weight: float = 0.0
```

2. Add prompting in `RecommenderAgent._profile_user()`:
```python
def _get_tempo_preference(self) -> float:
    return float(input("Target tempo (BPM): "))
```

3. Add scoring in `Recommender.calculate_score()`:
```python
if user.target_tempo is not None:
    tempo_distance = abs(song.tempo_bpm - user.target_tempo)
    # ...add points based on distance
```

### Modify Recommendation Count

Change in `config.py`:
```python
class AgentConfig:
    DEFAULT_K_RECOMMENDATIONS = 10  # Was 5
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"
**Solution**: Run from project root and use `python -m`:
```bash
cd /path/to/applied-ai-system-final
python -m src.agent
```

### "File 'data/songs.csv' not found"
**Solution**: Make sure you're in the project directory:
```bash
pwd  # Should show .../applied-ai-system-final
python -m src.agent
```

### "Virtual environment not activating"
**Solution**: Use the full activation path:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Logs not appearing
**Solution**: Check log directory exists:
```bash
ls -la logs/
# Should see agent_run_*.log files
```

---

## Testing

Run the test suite:

```bash
pytest tests/
```

Includes tests for:
- Song loading
- Scoring algorithm
- Recommendation ranking
- User profile creation

---

## Performance Notes

- **Song Loading**: ~10ms for 20 songs
- **Scoring**: ~100ms for 20 songs
- **First Recommendations**: <200ms
- **Refinement**: <150ms per adjustment

All times are on typical modern hardware.

---

## Reproducibility Checklist

✅ Unique run ID generated for each session  
✅ All user inputs logged with timestamps  
✅ Scoring algorithm deterministic (same inputs = same scores)  
✅ Session data exported to JSON for audit trail  
✅ Log file captures all decisions and adjustments  
✅ User profile snapshots saved before/after refinements  

To reproduce a session:
1. Use same user profile from `logs/session_RUNID.json`
2. Load same songs from `data/songs.csv`
3. Check `logs/agent_run_RUNID.log` for exact sequence of events

---

## Future Enhancements

Potential improvements for the agent:

- [ ] Multi-user profiles (save preferences)
- [ ] Collaborative filtering (what similar users liked)
- [ ] Feature importance explanation ("Energy weight: 40%")
- [ ] A/B testing framework for algorithm tweaks
- [ ] Integration with music APIs (Spotify, YouTube)
- [ ] Natural language processing for free-form preferences
- [ ] Reinforcement learning from user feedback over time
- [ ] Export recommendations to playlist

---

## License & Attribution

This agent is part of the CodePath Applied AI System course project.

---

**Questions or issues?** Check the logs directory first - `logs/agent_run_*.log` will have detailed information about what the agent did and why!
