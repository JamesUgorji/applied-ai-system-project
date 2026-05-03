# 🎵 Music Recommender Agent

An interactive agentic workflow that converses with users to understand their music preferences, generates personalized recommendations using a point-weighting algorithm, and iteratively refines results based on feedback.

## Quick Start

```bash
# Setup (first time only)
./setup.sh

# Run the interactive agent
source .venv/bin/activate
python -m src.agent
```

Or see a demo without manual input:
```bash
python3 demo_agent.py
```

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

## System Architecture

The agent follows a feedback loop pattern:

1. **User Profiling** - Conversational questions about music taste
2. **Generate Recommendations** - Score all 80 songs using point-weighting
3. **Refinement Loop** - User feedback iteratively improves recommendations
4. **Export & Save** - All results logged for reproducibility

See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for detailed component breakdown.

## Features

✅ **Reproducible** - Unique run ID, deterministic scoring, JSON export  
✅ **Logged** - Complete audit trail of all decisions  
✅ **Transparent** - Every recommendation includes reasoning  
✅ **Adaptive** - Iterative refinement based on user feedback  
✅ **Robust** - Error handling, input validation, graceful recovery  

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - 2-page cheat sheet with commands
- **[AGENT_GUIDE.md](AGENT_GUIDE.md)** - Complete 500+ line guide
- **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** - System diagram & data flow

## Dataset

- **80 songs** with diverse genres (pop, rock, ambient, jazz, hip-hop, etc.)
- **Mainstream artists** (The Weeknd, Ed Sheeran, Coldplay, Drake, etc.)
- **Rich attributes** - genre, mood, energy, tempo, valence, danceability, acousticness

## Scoring Algorithm

The agent uses a **point-weighting strategy**:

| Feature | Points | Notes |
|---------|--------|-------|
| Genre match (exact) | 0.75 | Fuzzy matching for similar genres |
| Mood match (exact) | 1.0 | Supports fuzzy matching |
| Energy alignment | 2.0 max | Within ±0.2 tolerance |
| Acoustic preference | 0.5 max | If user likes acoustic |
| **Maximum** | **3.75** | Perfect match score |

## Running Tests

```bash
pytest tests/
```

## Project Structure

```
├── src/
│   ├── agent.py          # RecommenderAgent - main workflow
│   ├── config.py         # Logging & configuration
│   ├── recommender.py    # Scoring engine
│   └── main.py           # Entry point with menu
├── data/
│   └── songs.csv         # 80-song dataset
├── logs/                 # Generated per run
│   ├── agent_run_*.log   # Detailed execution logs
│   └── session_*.json    # Reproducible session data
├── tests/
│   └── test_recommender.py
├── AGENT_GUIDE.md        # Complete documentation
├── QUICK_START.md        # Quick reference
├── SYSTEM_ARCHITECTURE.md # System diagram & components
├── setup.sh              # Setup script
└── requirements.txt      # Dependencies
```

## Key Components

- **Agent** (src/agent.py) - Orchestrates 4-phase workflow
- **Recommender** (src/recommender.py) - Scoring & ranking engine
- **Config** (src/config.py) - Centralized logging & settings
- **Retriever** (data/songs.csv) - Song catalog with 80 tracks

## Reproducibility

Every session generates:
- **logs/agent_run_TIMESTAMP.log** - Complete execution trace with all decisions
- **logs/session_TIMESTAMP.json** - User profile + final recommendations in JSON format

Load the session JSON and re-run with same songs → identical scores ✓

## Example Session

```
🎵 Welcome to the Music Recommender Agent!
📋 What's your favorite genre? lofi
😊 What mood are you in? focused
⚡ What energy level? 0.4
🎶 Do you like acoustic music? yes

1. 🎵 Focus Flow by LoRoom - Score: 3.75
   ➜ matches your lofi preference and has that focused vibe

2. 🎵 Midnight Coding by LoRoom - Score: 2.55
   ➜ matches your lofi preference

> more energetic
✅ Energy adjusted to 0.50
[Recommendations updated with new energy level]

> done
✅ Session saved to logs/session_20260503_101522.json
```
### Example 2
```
🎵 Welcome to the Music Recommender Agent!
==================================================

📋 Let's learn about your music taste!
--------------------------------------------------

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

🔍 Finding your top 5 recommendations...
--------------------------------------------------

1. 🎵 Focus Flow by LoRoom
   Score: 3.75
   ➜ matches your lofi preference and has that focused vibe

2. 🎵 Midnight Coding by LoRoom
   Score: 2.55
   ➜ matches your lofi preference

3. 🎵 Library Rain by Paper Lanterns
   Score: 2.25
   ➜ matches your lofi preference

4. 🎵 Mountain Echo by Folk Wanderer
   Score: 1.80
   ➜ matches adjusted focused mood

5. 🎵 Night Drive Loop by Neon Echo
   Score: 1.70
   ➜ offers an interesting combination of features

==================================================
💬 Refinement Mode
==================================================

> more energetic
✅ Energy adjusted to 0.50

🔄 Re-generating with new preference...

1. 🎵 Focus Flow by LoRoom
   Score: 2.75
   ...
   
> list

📊 Current Recommendations
==================================================

1. 🎵 Focus Flow by LoRoom
   ...

> done

==================================================
💾 Saving Your Session
==================================================

✅ Results saved to: logs/session_20260502_221903.json

📈 Session Summary
--------------------------------------------------
Run ID: 20260502_221903
Preferences: lofi (focused, energy: 0.5)
Recommendations generated: 5

Detailed logs saved to: logs/agent_run_20260502_221903.log
```



## Next Steps

For a complete walkthrough, see:
1. [QUICK_START.md](QUICK_START.md) - Start here for commands
2. [AGENT_GUIDE.md](AGENT_GUIDE.md) - Deep dive into features
3. [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - Understand the design

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

-> Name: Talk2Musi

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

-> This is model is for users who want to work more inclusive with AI when it comes to the recommendations of their songs. 
---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

-> This model usese a Agentic workflow, where the AI suggests 5 songs to the user from of a catalog based on the user's preferred genre, mood, and energy level. After it takes feedback from the user on the reccomendations, and edits the scoring of the different preferences of the user to make suggestions. 

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

-> There are ~80 songs in the the catolog of data, I changed all of the songs, and have a variety of different music generes and mood represented. 
---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

-> When it comes to strength, it's really engaging and interactive, make it seem like you're in control. I don't really see any trade-offs. If you want to use the recommender without the AI, you still can. 

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

-> For the design decision, I figured it would be more interactive and engaging to have the user have control of the way it get's recommended music. In addition to be able to judge and adjust the way the AI recommended songs. 
---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

-> I want to allow for a user to have different playlist that gets recommended based on their prefered playlist genere and past music taste. 

Also adding more features. 

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

-> I think a lot worked. The system is interactive, it recommends real songs, allows the user to be in control. However I realized that there's a lot more to do to make this feel like the user can actually coustimize their own listening experience. It would take more engineeirng with prompts and editing the AI. 

This taught me that lot of building these project and AI model is really just testing and experimenting. Using it for yourself really shows you what can be optimized, what works, and what doesn't

There are a lot of limitation when it comes to fully customizng the user experience with the AI, such as being able to request a different recommendation for a specific song, and not all of them. 

Since this is a music reommendor I don't see it as being able to really be misused. There is no personal data or information being used outside of the user perferences. 
