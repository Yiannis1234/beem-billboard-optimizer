# 📊 Calculation Logic Explanation

## How Success Scores Are Calculated

### Formula Breakdown

**Final Success Score = Base Score + Factor Boost + Weather Adjustments + Traffic Boost + Places Boost + Campaign Boost**

---

## 1. Base Score from Footfall

**Formula:** `base_score = min(60, (footfall_daily / 10000))`

**Explanation:**
- Takes daily footfall and divides by 10,000
- Maximum base score is capped at 60 points
- Requires 600,000+ daily footfall to reach max

**Examples:**
- 120,000 daily footfall → 120,000 / 10,000 = **12 points**
- 400,000 daily footfall → 400,000 / 10,000 = **40 points** (capped at 60)
- 600,000+ daily footfall → **60 points** (maximum)

**Issue:** ⚠️ This might be too low! For areas with 120,000 footfall, base score is only 12, which seems low.

---

## 2. Factor Boost

**Formula:** Adds points based on area characteristics

| Factor | Points Added |
|--------|--------------|
| High Traffic | +15 |
| Business District | +12 |
| Transport Hub | +12 |
| Affluent Audience | +8 |
| Student Area | +8 |
| Shopping Area | +8 |
| Creative Area | +5 |

**Maximum possible:** 15 + 12 + 12 + 8 + 8 + 8 + 5 = **68 points**

**Example:**
- Albert Square has: high_traffic, business_district, transport_hub, affluent_audience, shopping_area, brand_conscious
- Factor boost = 15 + 12 + 12 + 8 + 8 = **55 points**

---

## 3. Weather Adjustments

**Formula:** Score delta and impression percentage change based on weather

**Score Adjustments:**
- Very clear visibility (≥9km): +4 points
- Good visibility (6-9km): +2 points
- Low visibility (3-6km): -3 points
- Very poor visibility (<3km): -6 points

**Impression Adjustments:**
- Sunny/Clear: +4% impressions
- Rain: -6% impressions
- Snow: -10% impressions
- Storm: -12% impressions
- Comfortable temp (12-22°C): +3% impressions
- Very cold (<3°C): -8% impressions
- Very hot (>28°C): -4% impressions

**Range:** Typically -10 to +10 points, -15% to +10% impressions

---

## 4. Traffic Boost

**Formula:** Based on congestion level

| Congestion Level | Points Added |
|------------------|--------------|
| Heavy | +8 |
| Moderate | +5 |
| Light/Free Flow | 0 |

---

## 5. Google Places Boost

**Formula:** Based on popularity, rating, and reviews

- **Popularity Score:** (popularity_score / 100) * 10 = 0-10 points
- **Rating Boost:** 
  - 4.5+ stars: +3 points
  - 4.0-4.5 stars: +2 points
  - 3.5-4.0 stars: +1 point
- **Review Boost:**
  - 1000+ reviews: +2 points
  - 100-1000 reviews: +1 point

**Maximum:** 15 points

---

## 6. Campaign Boost (Audience Match)

**Formula:** Adjusts score based on how well area matches campaign

**Calculation:**
- 80%+ match: +9 to +15 points
- 60-79% match: +2 to +9 points
- 40-59% match: 0 points (neutral)
- <40% match: -2 to -10 points

**Final Score Range:** 25-98 (min 25, max 98)

---

## 7. Impressions Per Hour

**Formula:** `base_impressions_per_hour = (footfall_daily / 24) * 0.15`

**Explanation:**
- Divides daily footfall by 24 hours
- Assumes 15% of people passing by will see the ad
- Then adjusts by weather percentage

**Examples:**
- 120,000 daily footfall:
  - Hourly: 120,000 / 24 = 5,000 people/hour
  - Impressions: 5,000 * 0.15 = **750 impressions/hour**
  
- 400,000 daily footfall:
  - Hourly: 400,000 / 24 = 16,667 people/hour
  - Impressions: 16,667 * 0.15 = **2,500 impressions/hour**

**Weather Adjustment:**
- If weather gives +4%: 750 * 1.04 = **780 impressions/hour**
- If weather gives -6%: 750 * 0.94 = **705 impressions/hour**

---

## Complete Example Calculation

**Location:** Albert Square, Manchester
- Daily footfall: 120,000
- Factors: high_traffic, business_district, transport_hub, affluent_audience, shopping_area, brand_conscious
- Weather: Sunny, 15°C, good visibility
- Traffic: Moderate congestion
- Google Places: Rating 4.2, 500 reviews

**Step-by-step:**

1. **Base Score:** 120,000 / 10,000 = **12 points**

2. **Factor Boost:** 15 + 12 + 12 + 8 + 8 = **55 points**

3. **Weather:**
   - Sunny: +3 points, +4% impressions
   - Good visibility: +2 points
   - Comfortable temp: +3 points, +3% impressions
   - **Total:** +8 points, +7% impressions

4. **Traffic:** Moderate = **+5 points**

5. **Places:** 
   - Popularity: ~70/100 = 7 points
   - Rating 4.2: +2 points
   - 500 reviews: +1 point
   - **Total:** +10 points

6. **Base Success Score:** 12 + 55 + 8 + 5 + 10 = **90 points** (capped at 95)

7. **Campaign Boost** (if Luxury Fashion, 100% match):
   - Match: 100%
   - Boost: (1.0 - 0.5) * 30 = +15 points
   - **Final Score:** min(98, 90 + 15) = **98 points**

8. **Impressions:**
   - Base: (120,000 / 24) * 0.15 = 750/hour
   - Weather adjusted: 750 * 1.07 = **803 impressions/hour**

---

## Potential Issues & Improvements

### Issue 1: Base Score Too Low
**Problem:** Base score of 12 for 120k footfall seems low
**Current:** `footfall_daily / 10000`
**Suggestion:** Could use logarithmic scale or higher multiplier

### Issue 2: 15% View Rate
**Problem:** 15% of people seeing the ad might be too high
**Current:** 0.15 (15%)
**Suggestion:** Industry standard is 5-10% for billboards

### Issue 3: Factor Boost Can Exceed Base Score
**Problem:** Factor boost (55) is much higher than base score (12)
**Current:** Factors dominate the score
**Suggestion:** Balance better between footfall and factors

### Issue 4: No Time-of-Day Variation
**Problem:** Impressions are averaged across 24 hours
**Suggestion:** Could add peak hours (rush hour, lunch) with higher rates

---

## Recommendations

1. **Adjust Base Score Formula:**
   - Use: `min(40, (footfall_daily / 5000))` for better scaling
   - Or: `min(50, log(footfall_daily / 1000) * 10)` for logarithmic scaling

2. **Adjust View Rate:**
   - Change from 15% to 8-10% for more realistic impressions

3. **Add Peak Hours:**
   - Rush hour (7-9am, 5-7pm): 1.5x multiplier
   - Lunch (12-2pm): 1.2x multiplier
   - Off-peak: 0.7x multiplier

4. **Balance Factors:**
   - Reduce factor boost or increase base score weight

---

## Current Formula Summary

```python
# Base Score (0-60 points)
base_score = min(60, footfall_daily / 10000)

# Factor Boost (0-68 points)
factor_boost = sum of all active factors

# Weather Delta (-10 to +10 points typically)
weather_delta = calculated from visibility, temp, condition

# Traffic Boost (0-8 points)
traffic_boost = 0-8 based on congestion

# Places Boost (0-15 points)
places_boost = popularity + rating + reviews

# Campaign Boost (-10 to +15 points)
campaign_boost = based on audience match

# Final Score (25-98)
final_score = base + factors + weather + traffic + places + campaign
```

**Total Possible Range:** 25-98 points

---

## Verification

To verify calculations are correct, check:
1. ✅ Base scores scale with footfall
2. ✅ Factor boosts add correctly
3. ✅ Weather adjustments are reasonable (-10 to +10)
4. ✅ Impressions formula: (footfall/24) * view_rate
5. ✅ Campaign boost scales with match percentage
6. ⚠️ Base score might be too low relative to factors
7. ⚠️ 15% view rate might be optimistic

