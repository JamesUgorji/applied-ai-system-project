# 🎵 System Architecture & Data Flow

## System Diagram Overview

The interactive music recommender agent is composed of 8 main components working together in a feedback loop:

```
USER INPUT → AGENT → RETRIEVER → SCORER → RANKER → OUTPUT
                                                         ↓
                                                   HUMAN REVIEW
                                                         ↓
                                                    EVALUATOR
                                                         ↓
                                                      LOGGER
                                                         ↓
                                                   OUTPUT FILES
                                                         ↓
                                                     TESTER
                                                         ↓
                                                  FINAL RESULT
```

---

## Component Breakdown

### 1️⃣ **USER INPUT** 
**Type:** Entry Point  
**Role:** Gather initial preferences  
**Input:** Conversational questions
- "What's your favorite genre?"
- "What mood are you in?"
- "What energy level? (0-1)"
- "Do you like acoustic music?"

**Output:** Raw user preferences (strings, floats, booleans)

**Code Location:** `src/agent.py` → `_profile_user()`

---

### 2️⃣ **AGENT** 
**Type:** Orchestrator (RecommenderAgent class)  
**Role:** Coordinate all workflow phases  
**Responsibilities:**
- Manage user profiling (Phase 1)
- Control recommendation generation (Phase 2)
- Drive refinement loop (Phase 3)
- Trigger result export (Phase 4)

**Key Methods:**
- `run()` - Main workflow orchestration
- `_profile_user()` - Conversational preference gathering
- `_generate_recommendations()` - Score and rank songs
- `_refinement_loop()` - Interactive feedback loop
- `_export_results()` - Save session data

**Code Location:** `src/agent.py` → `RecommenderAgent` class

---

### 3️⃣ **RETRIEVER** 
**Type:** Data Source  
**Role:** Load and provide song catalog  
**Data Source:** `data/songs.csv` (80 songs)

**Returns:** List of Song objects with attributes:
```
Song {
  id: int
  title: str
  artist: str
  genre: str
  mood: str
  energy: float (0-1)
  tempo_bpm: float
  valence: float (0-1)
  danceability: float (0-1)
  acousticness: float (0-1)
}
```

**Code Location:** `src/recommender.py` → `load_songs()`

---

### 4️⃣ **SCORER** 
**Type:** Algorithm Engine  
**Role:** Calculate compatibility scores  
**Algorithm:** Point-Weighting System

**Scoring Breakdown:**
```
Total Score = Genre Points + Mood Points + Energy Points + Acoustic Points

Genre:
  - Exact match: 0.75 points
  - Fuzzy match (>70% similarity): 0.375 points
  - No match: 0 points

Mood:
  - Exact match: 1.0 points
  - Fuzzy match: 0.5 points
  - No match: 0 points

Energy: (max 2.0 points)
  - Within ±0.2 of target: Full linear scoring
  - Outside tolerance: Exponential decay

Acoustic: (if user likes acoustic)
  - 0.5 × acousticness value (max 0.5 points)

Maximum Total: 3.75 points
```

**Code Location:** `src/recommender.py` → `Recommender.calculate_score()`

---

### 5️⃣ **RANKER** 
**Type:** Sorter  
**Role:** Order songs by score  
**Process:**
1. Take all scored songs
2. Sort descending by score
3. Extract top-K (default: 5)
4. Return ranked list

**Code Location:** `src/agent.py` → `_generate_recommendations()`

---

### 6️⃣ **OUTPUT (Display)**
**Type:** User Interface  
**Role:** Present recommendations clearly  
**Format:**
```
🎵 Song Title by Artist Name
   Score: X.XX
   ➜ Explanation: Why this song matched
```

**Example Output:**
```
1. 🎵 Focus Flow by LoRoom
   Score: 3.75
   ➜ matches your lofi preference and has that focused vibe

2. 🎵 Midnight Coding by LoRoom
   Score: 2.55
   ➜ matches your lofi preference
```

**Code Location:** `src/agent.py` → `_generate_recommendations()` and `_show_recommendations()`

---

### 7️⃣ **HUMAN REVIEW** 
**Type:** Feedback Loop  
**Role:** User provides iterative feedback  
**User Capabilities:**
- View current recommendations (`list`)
- Request adjustments (`more energetic`, `less acoustic`)
- Exit refinement (`done`)

**Why This Matters:**
- Users don't always know their exact preferences upfront
- Iterative refinement allows discovery
- Transparent explanations build trust
- User feedback trains system understanding

**Code Location:** `src/agent.py` → `_refinement_loop()`

---

### 8️⃣ **EVALUATOR** 
**Type:** Feedback Processor  
**Role:** Apply user feedback and re-score  
**Process:**
1. Parse user feedback ("more energetic")
2. Identify affected preference dimension (energy)
3. Adjust user profile (±0.1)
4. Re-score all songs with new profile
5. Return updated recommendations

**Tracked Changes:**
- Energy adjustment
- Acoustic preference toggle
- Any preference modifications logged

**Code Location:** `src/agent.py` → `_adjust_preference()` and `_refinement_loop()`

---

### 9️⃣ **LOGGER** 
**Type:** Data Persistence  
**Role:** Record all session data for reproducibility  
**Logs Two Types of Data:**

**A. Detailed Execution Log** (`logs/agent_run_TIMESTAMP.log`)
```
2026-05-03 10:15:22,123 - recommender_agent - INFO - Agent initialized with 80 songs
2026-05-03 10:15:23,456 - recommender_agent - INFO - User selected genre: pop
2026-05-03 10:15:24,789 - recommender_agent - INFO - Generated 5 recommendations
2026-05-03 10:15:30,001 - recommender_agent - INFO - Adjusted energy to 0.50
2026-05-03 10:15:32,234 - recommender_agent - INFO - Session data saved
```

**B. Session Snapshot** (`logs/session_TIMESTAMP.json`)
```json
{
  "run_id": "20260503_101522",
  "timestamp": "2026-05-03T10:15:22.123456",
  "user_profile": {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.5,
    "likes_acoustic": false
  },
  "recommendations": [
    {
      "title": "Levitating",
      "artist": "Dua Lipa",
      "score": 3.45,
      "explanation": "matches your pop preference"
    }
  ]
}
```

**Code Location:** `src/config.py` → `save_session_data()`

---

### 🔟 **TESTER** 
**Type:** Quality Assurance  
**Role:** Verify system correctness and reproducibility  
**Testing Areas:**

**1. Determinism Check:**
- Load same user profile
- Score against same songs
- Verify identical scores

**2. Reproducibility Verification:**
- Load session JSON from logs
- Re-run exact same workflow
- Confirm recommendations match

**3. Algorithm Validation:**
- Score calculation correct?
- Ranking order right?
- Explanations accurate?

**4. Edge Cases:**
- Invalid genre → fuzzy match works
- Multiple adjustments → cumulative
- Large catalog → performance OK

**Example Verification:**
```bash
# Load saved session
cat logs/session_20260503_101522.json

# Verify scores are reproducible
python3 -c "
from src.recommender import *
profile = UserProfile(...)  # from JSON
songs = load_songs(...)     # same CSV
# Re-calculate scores
# Assert scores match logged values
"
```

**Code Location:** Manual testing via logs inspection

---

## Data Flow Through System

### **Phase 1: User Profiling** 
```
User answers questions
    ↓
Agent captures responses
    ↓
UserProfile object created
    ↓
Profile logged (DEBUG level)
```

### **Phase 2: Generate Recommendations**
```
Agent loads songs from CSV
    ↓
Retriever returns 80 Song objects
    ↓
Scorer.calculate_score() called for each song
    ↓
Scores collected: [(Song, score), ...]
    ↓
Ranker sorts by score descending
    ↓
Top-5 extracted
    ↓
Explanations generated
    ↓
Results displayed to user
    ↓ 
Recommendations logged
```

### **Phase 3: Refinement Loop**
```
User sees recommendations
    ↓
User provides feedback: "more energetic"
    ↓
Evaluator parses feedback
    ↓
UserProfile.target_energy adjusted (0.4 → 0.5)
    ↓
Scorer re-scores all songs
    ↓
Ranker re-ranks
    ↓
Updated recommendations displayed
    ↓
Change logged
    ↓
Loop back to feedback (if "done" not given)
```

### **Phase 4: Export & Validation**
```
User says "done"
    ↓
Final recommendations collected
    ↓
Logger creates session JSON
    ↓
Logger creates execution log file
    ↓
Tester can verify by:
  1. Reading JSON
  2. Re-running same profile
  3. Comparing scores
  ↓
✅ Reproducibility confirmed
```

---

## Human-in-the-Loop Integration

### **Where Humans Are Involved:**

| Stage | Role | Method |
|-------|------|--------|
| **Input** | Provide preferences | Conversational Q&A |
| **Review** | Judge recommendations | Visual inspection |
| **Feedback** | Refine results | Chat commands |
| **Testing** | Verify correctness | Log inspection |
| **Audit** | Check reproducibility | JSON review |

### **Why Humans Matter:**

✅ **Validation** - Confirms recommendations feel right  
✅ **Feedback** - Improves system through iteration  
✅ **Testing** - Catches algorithmic errors  
✅ **Auditing** - Ensures reproducibility for transparency  
✅ **Explanation** - Understands why recommendations were made  

---

## System Guarantees

### ✅ **Reproducibility**
Every run produces identical recommendations given:
- Same user profile
- Same song catalog
- Same algorithm (deterministic)

### ✅ **Traceability**
All decisions recorded:
- User inputs → logs
- Algorithm choices → logs
- Adjustments → logs
- Final output → JSON

### ✅ **Explainability**
Every recommendation includes reasoning:
- "Matches your X preference"
- "Has your Y mood"
- "Close to target Z energy"

### ✅ **Error Resilience**
Graceful handling of:
- Invalid inputs (re-prompt)
- Missing files (inform user)
- Edge cases (fuzzy matching)

---

## Performance Characteristics

| Operation | Time | Scale |
|-----------|------|-------|
| Load 80 songs | ~10ms | Linear with song count |
| Score all songs | ~50-100ms | Linear with song count |
| Rank/sort | ~5ms | O(n log n) |
| First recommendations | <200ms | Typically sub-second |
| Refinement re-score | <150ms | Same as scoring |

---

## Extension Points

Future enhancements could add:

1. **Richer Scorer**
   - Add more dimensions (tempo, valence, danceability)
   - Use machine learning instead of rules

2. **Better Retriever**
   - Connect to music APIs (Spotify, Apple Music)
   - Filter by release date, language, etc.

3. **Smarter Evaluator**
   - Learn from user feedback over time
   - Predict next adjustment automatically

4. **Advanced Tester**
   - A/B test scoring strategies
   - Measure user satisfaction
   - Automated regression testing

---

## Summary

The system follows a classic **AI loop pattern**:

```
UNDERSTAND → ACT → OBSERVE → EVALUATE → IMPROVE → REPEAT
```

With humans involved at **every critical step**:
- 👤 Input phase: User provides preferences
- ✅ Review phase: User validates recommendations
- 💬 Feedback phase: User guides refinement
- 🧪 Testing phase: Human ensures correctness
- 📋 Audit phase: Human reviews logs

This creates a **trustworthy, transparent AI system** that users can understand, verify, and improve over time.
