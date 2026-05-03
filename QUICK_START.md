# 🎵 Interactive Agent - Quick Reference

## 🚀 Getting Started

```bash
# First time setup (2 minutes)
./setup.sh

# Every time: Activate environment
source .venv/bin/activate

# Run the interactive agent
python -m src.agent
```

## 📋 Agent Commands (Phase 3: Refinement)

| Command | Effect | Example |
|---------|--------|---------|
| `more <feature>` | Increase preference | `more energetic` |
| `less <feature>` | Decrease preference | `less acoustic` |
| `list` | Show recommendations | `list` |
| `done` | Exit refinement | `done` |

### Supported Features
- **energy** - Song energy level (0-1 scale)
- **acoustic** - Acousticness preference (on/off)

## 📊 Workflow at a Glance

```
Phase 1: Answer Questions (2-3 minutes)
┌─ What's your favorite genre?
├─ What mood are you in?
├─ What energy level? (0-1 or low/medium/high)
└─ Do you like acoustic music?

Phase 2: See Recommendations (automatic)
┌─ Agent scores all 20 songs
├─ Shows top 5 with explanations
└─ Each song shows: Title, Artist, Score, Why

Phase 3: Refine Results (optional)
┌─ Give feedback ("more energetic", etc.)
├─ Agent re-scores all songs
└─ Recommendations update in real-time

Phase 4: Results Saved (automatic)
┌─ Log file: logs/agent_run_TIMESTAMP.log
├─ Session data: logs/session_TIMESTAMP.json
└─ Ready for future reference
```

## 📁 What Gets Saved

After each session, check:

```bash
# See all sessions
ls -lh logs/

# View detailed log
cat logs/agent_run_*.log

# View session data (JSON)
cat logs/session_*.json | python -m json.tool

# Find latest session
ls -lht logs/ | head -2
```

## 🎯 Example Session

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

## 🔄 Running the Demo

```bash
python3 demo_agent.py
```

Shows the agent in action with pre-set preferences. Great for testing!

## 📜 Understanding Log Entries

```
INFO: Agent initialized with 20 songs
→ Agent loaded all songs successfully

INFO: User profile created: UserProfile(...)
→ User's preferences captured

INFO: Generated 5 recommendations
→ Scored all songs and ranked them

INFO: Adjusted energy to 0.50
→ User made a refinement

INFO: Session data saved to logs/session_*.json
→ All results exported
```

## 🎵 Sample Output Interpretation

**Score: 3.75** out of max 3.75
- Perfect match on genre (0.75) ✓
- Perfect match on mood (1.0) ✓
- Perfect energy match (2.0) ✓

**Score: 2.55**
- Genre match (0.75) ✓
- Mood partial match (0.5)
- Energy close (1.3)

## 🛠️ If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run from project root with `python -m src.agent` |
| `File not found` | Make sure `data/songs.csv` exists |
| Venv not activating | Use full path: `source .venv/bin/activate` |
| Logs missing | Check `logs/` directory exists |
| Agent crashes | Check `logs/agent_run_*.log` for error details |

## 📱 Energy Level Guide

- **Low (0.0-0.3)**: Study music, meditation, sleeping, background
- **Medium (0.3-0.65)**: Everyday listening, working, relaxing, focused work
- **High (0.65-1.0)**: Workouts, parties, energetic activities, running

## 🎯 Pro Tips

1. **Start broad**: Pick main genre/mood, refine from there
2. **Use refinement**: Most power comes from "more/less energetic"
3. **Check logs**: `logs/agent_run_*.json` has all decisions
4. **Replay sessions**: Load saved JSON to see exact recommendations again
5. **Multiple runs**: Each gets unique ID, so you can compare preferences

## 📦 Contents of Session JSON

```json
{
  "run_id": "timestamp",
  "timestamp": "ISO 8601 datetime",
  "user_profile": {
    "favorite_genre": "your choice",
    "favorite_mood": "your choice",
    "target_energy": 0.4,
    "likes_acoustic": true
  },
  "recommendations": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "score": 3.75,
      "explanation": "Why this song matched"
    }
  ]
}
```

Perfect for auditing, analysis, or feeding into other systems!

---

**Need more help?** See [AGENT_GUIDE.md](AGENT_GUIDE.md) for complete documentation.
