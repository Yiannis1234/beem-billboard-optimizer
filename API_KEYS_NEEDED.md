# 🔑 API Keys Needed for BritMetrics

## ✅ Currently Active API Keys

### 1. WeatherAPI.com
**Status:** ✅ Active (hardcoded in code)
**Key:** `f70bd534000447b2a14202431252303`
**Location:** `backend/api_services.py` line 21
**Cost:** Free tier available
**Action:** ✅ No key needed - already working

### 2. TomTom Traffic API
**Status:** ✅ Active (hardcoded in code)
**Key:** `sljp3YAvFa7J3EalnGslYfnSCZg6VQUg`
**Location:** `backend/api_services.py` line 71
**Cost:** Free tier: 2,500 requests/day
**Action:** ✅ No key needed - already working

### 3. Google Places API
**Status:** ✅ Active (just integrated)
**Key:** `AIzaSyDOR3SP5wXTznBEscqYcrJHlMom8bR18lw`
**Location:** `backend/api_services.py` line 161
**Cost:** $200 free credit/month, then $0.017/request
**Action:** ✅ No key needed - already working

### 4. Stripe Payment API
**Status:** ⚠️ Needs configuration
**Keys Needed:**
- `STRIPE_PUBLISHABLE_KEY` (for frontend)
- `STRIPE_SECRET_KEY` (for backend)
**Location:** `.env` file (not in code for security)
**Cost:** 2.9% + $0.30 per transaction
**Action:** ⚠️ **NEEDS SETUP** - Get from https://dashboard.stripe.com/apikeys

---

## 🔴 API Keys Needed for Priority Integrations

### 1. UK Census Data ⭐⭐⭐ (FREE - HIGHEST PRIORITY)
**Status:** ❌ Not integrated yet
**Key Needed:** ❌ **NO KEY NEEDED** - It's free open data!
**How to Access:**
- ONS API: https://www.ons.gov.uk/developer (no registration needed)
- Nomis API: https://www.nomisweb.co.uk/api/v01/ (free registration)
**Action:** ✅ **NO KEY NEEDED** - Can implement today!

---

### 2. Eventbrite API ⭐⭐ (HIGH PRIORITY for Events)
**Status:** ❌ Not integrated yet
**Key Needed:** ✅ **YES - Need OAuth Token**
**How to Get:**
1. Go to: https://www.eventbrite.com/platform/api/
2. Sign up for Eventbrite Developer account
3. Create an app
4. Get OAuth Token
**Cost:** FREE for basic access
**Action:** 🔴 **NEED KEY** - Get from Eventbrite Developer Portal

---

### 3. Facebook Events API ⭐ (MEDIUM PRIORITY)
**Status:** ❌ Not integrated yet
**Key Needed:** ✅ **YES - Need Access Token**
**How to Get:**
1. Go to: https://developers.facebook.com/
2. Create a Facebook App
3. Get Access Token (requires app review for production)
**Cost:** FREE
**Action:** 🔴 **NEED TOKEN** - Get from Facebook Developers

---

### 4. Twitter API ⭐ (LOW PRIORITY)
**Status:** ❌ Not integrated yet
**Key Needed:** ✅ **YES - Need Bearer Token**
**How to Get:**
1. Go to: https://developer.twitter.com/
2. Apply for Developer account
3. Create an app
4. Get Bearer Token
**Cost:** Free tier limited, paid plans available
**Action:** 🔴 **NEED TOKEN** - Get from Twitter Developer Portal

---

## 📋 Summary: What You Need

### ✅ Already Have (No Action Needed):
1. ✅ WeatherAPI key - Working
2. ✅ TomTom Traffic key - Working
3. ✅ Google Places key - Working
4. ✅ Stripe keys - Need to set up (optional for payments)

### 🔴 Need to Get (Priority Order):

#### **Priority 1: UK Census Data**
- **Key Needed:** ❌ NO KEY - FREE!
- **Action:** ✅ Can implement immediately - no keys needed

#### **Priority 2: Eventbrite API** (if targeting events)
- **Key Needed:** ✅ YES - OAuth Token
- **Where:** https://www.eventbrite.com/platform/api/
- **Cost:** FREE
- **Action:** 🔴 Get OAuth token from Eventbrite

#### **Priority 3: Facebook Events API** (optional)
- **Key Needed:** ✅ YES - Access Token
- **Where:** https://developers.facebook.com/
- **Cost:** FREE
- **Action:** 🔴 Get access token from Facebook

#### **Priority 4: Twitter API** (optional, nice to have)
- **Key Needed:** ✅ YES - Bearer Token
- **Where:** https://developer.twitter.com/
- **Cost:** FREE tier available
- **Action:** 🔴 Get bearer token from Twitter

---

## 🔐 Security Best Practices

### Current Setup (⚠️ Needs Improvement):
- API keys are **hardcoded** in the code
- This is **NOT SECURE** for production

### Recommended Setup:

1. **Create `.env` file** (already in `.gitignore`):
```bash
# Weather API
WEATHER_API_KEY=f70bd534000447b2a14202431252303

# TomTom Traffic API
TOMTOM_API_KEY=sljp3YAvFa7J3EalnGslYfnSCZg6VQUg

# Google Places API
GOOGLE_PLACES_API_KEY=AIzaSyDOR3SP5wXTznBEscqYcrJHlMom8bR18lw

# Stripe (if using payments)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Future APIs
EVENTBRITE_OAUTH_TOKEN=your_token_here
FACEBOOK_ACCESS_TOKEN=your_token_here
TWITTER_BEARER_TOKEN=your_token_here
```

2. **Update code to use environment variables:**
   - Already done for Google Places ✅
   - Should do for Weather and TomTom ⚠️

3. **Never commit `.env` to Git:**
   - Already in `.gitignore` ✅

---

## 🎯 Recommended Action Plan

### Immediate (No Keys Needed):
1. ✅ **UK Census Data** - Implement today (FREE, no keys)

### Short Term (1-2 weeks):
2. 🔴 **Eventbrite API** - Get OAuth token if targeting events
3. ⚠️ **Move API keys to `.env`** - Better security

### Long Term (Optional):
4. 🔴 **Facebook Events API** - If needed
5. 🔴 **Twitter API** - If needed for sentiment

---

## 📞 Quick Reference

| API | Key Needed? | Where to Get | Cost | Priority |
|-----|-------------|--------------|------|----------|
| WeatherAPI | ✅ Already have | N/A | Free | ✅ Working |
| TomTom | ✅ Already have | N/A | Free | ✅ Working |
| Google Places | ✅ Already have | N/A | $200 free/month | ✅ Working |
| UK Census | ❌ NO | N/A | FREE | ⭐⭐⭐ Implement now |
| Eventbrite | 🔴 YES | eventbrite.com/platform/api | FREE | ⭐⭐ High |
| Facebook Events | 🔴 YES | developers.facebook.com | FREE | ⭐ Medium |
| Twitter | 🔴 YES | developer.twitter.com | Free tier | ⭐ Low |
| Stripe | 🔴 YES | dashboard.stripe.com | 2.9% fee | ⚠️ Optional |

---

## 💡 Next Steps

1. **UK Census Data** - ✅ Can do NOW (no key needed!)
2. **Eventbrite** - Get OAuth token if you want event features
3. **Security** - Move all keys to `.env` file
4. **Facebook/Twitter** - Get later if needed

**Most important:** UK Census Data is FREE and needs NO KEY - can implement immediately!

