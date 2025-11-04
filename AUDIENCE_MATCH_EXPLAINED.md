# Audience Match - How It Works

## Overview
The audience match feature calculates how well a location's demographics match your campaign's target audience. It ranges from 0% (poor match) to 100% (perfect match).

## How It Works

### Step 1: Campaign Selection
When you select a campaign type (e.g., "Luxury Fashion Brand"), the system identifies the ideal demographic factors for that campaign:
- **Luxury Fashion Brand** looks for: `affluent_audience`, `business_district`, `shopping_area`, `brand_conscious`
- **Tech Startup** looks for: `student_area`, `creative_area`, `university_district`, `young_audience`
- And so on for each campaign type...

### Step 2: Area Analysis
Each location (like "Albert Square" or "Oxford Road") has specific demographic characteristics stored in the system:
- **Albert Square** has: `affluent_audience=True`, `business_district=True`, `shopping_area=True`, `brand_conscious=True`
- **Oxford Road** has: `student_area=True`, `university_district=True`, `young_audience=True`

### Step 3: Match Calculation
The system compares the campaign's ideal factors with the area's actual factors:

1. **Direct Matches**: Each matching factor counts as 1.0
   - Example: If campaign wants `affluent_audience` and area has it → +1.0

2. **Partial Matches**: Related factors count as 0.3-0.5 (smart matching)
   - Example: Campaign wants `brand_conscious`, area has `affluent_audience` → +0.5 (partial match)
   - Example: Campaign wants `young_audience`, area has `student_area` → +0.5 (partial match)

3. **Final Score**: `(total_matches / total_ideal_factors) × 100`
   - Perfect match (all 4 factors match) = 100%
   - Good match (3 out of 4 factors) = 75%
   - Moderate match (2 out of 4 factors) = 50%
   - Poor match (1 or 0 factors) = 0-25%

## Example Scenarios

### Perfect Match (100%)
- **Campaign**: Luxury Fashion Brand
- **Area**: Albert Square
- **Match**: All 4 ideal factors present → 100%

### Good Match (75-85%)
- **Campaign**: Tech Startup
- **Area**: Oxford Road
- **Match**: 3 direct matches + 1 partial match → ~82%

### Poor Match (0-25%)
- **Campaign**: Tech Startup
- **Area**: Chorlton (family suburb)
- **Match**: No relevant factors → 0%

## Impact on Success Score

The audience match score directly affects the overall success score:
- **High match (80%+)**: Adds +9 to +15 points to the base score
- **Good match (60-79%)**: Adds +2 to +9 points
- **Moderate match (40-59%)**: Neutral (no change)
- **Low match (<40%)**: Reduces score by -2 to -10 points

## Why It's Important

1. **Better Targeting**: Know which areas have your target audience
2. **Higher ROI**: Better match = higher engagement = better results
3. **Smart Recommendations**: Get personalized tips for each location
4. **Audience Size**: See how many of your target demographic will see your ad per hour

## Testing

Run the test script to verify everything works:
```bash
python3 test_audience_match.py
```

This will show you:
- Examples of perfect, good, and poor matches
- How different campaigns match different areas
- Full prediction flow with real API data

## Current Status

✅ **Working Correctly** - All tests pass
✅ **Variation in Scores** - Different areas show different match percentages (0-100%)
✅ **Smart Matching** - Partial matches work correctly
✅ **API Integration** - Weather and Traffic APIs are functioning

