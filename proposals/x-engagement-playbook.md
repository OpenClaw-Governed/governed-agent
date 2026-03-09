# X Engagement Playbook — @OpenClawGVRND

*Compiled: 2026-03-09*
*Sources: X Developer Policy, X Automation Rules (updated Oct 2025), OpenTweet 2026 guide, SocialRails 2026 guide, Google AI Overview best practices, Vynta AI bot compliance*

---

## Part 1: Metrics That Matter

### Account Growth Metrics (Weekly)
| Metric | What It Tells Us | Target (Month 1) |
|--------|-----------------|-------------------|
| **Follower growth rate** | Organic reach expanding | +50/week |
| **Follower-to-following ratio** | Authority signal | >0.5:1 by month 2 |
| **Profile visits** | Discovery/curiosity | Track baseline |

### Engagement Metrics (Per Post)
| Metric | What It Tells Us | Target |
|--------|-----------------|--------|
| **Engagement rate** | (likes + replies + retweets + quotes) / impressions | >2% (industry avg 0.5-1%) |
| **Reply rate** | Conversations started | >0.5% |
| **Quote tweet rate** | Content worth commenting on | Track — this is the gold metric |
| **Link click-through rate** | Repo/site traffic driven | >1% |
| **Bookmark rate** | Content worth saving (X weights this heavily in algo) | Track |

### Content Performance Metrics (Daily)
| Metric | What It Tells Us | Target |
|--------|-----------------|--------|
| **Impressions per post** | Algorithmic reach | Track baseline, optimize |
| **Best-performing post type** | What resonates (thread vs single, technical vs narrative) | Identify by week 2 |
| **Engagement by time of day** | When our audience is active | Optimize posting schedule |
| **Reply-to-post ratio** | Are we talking WITH people or AT them | >30% replies vs original posts |

### Governance-Specific Metrics (Unique to Us)
| Metric | What It Tells Us | Target |
|--------|-----------------|--------|
| **Draft-to-approval rate** | How many drafts JB approves vs kills | Track — calibration signal |
| **Time-to-approval** | Workflow efficiency | <30 min during operating hours |
| **Approval-to-post latency** | How fast we execute after approval | <2 min |
| **Governance receipt verification clicks** | Are people checking the repo | Track |
| **Stream queue → engagement conversion** | How many caught tweets we actually respond to | Track |

### Budget Metrics (Daily)
| Metric | Limit |
|--------|-------|
| **Daily API spend** | <$2/day |
| **Monthly API spend** | <$50 |
| **Credit balance** | Alert at <$10 |
| **Cost per engagement** | Track — should decrease over time |

---

## Part 2: Best Practices (Industry Consensus, 2025-2026)

### What X Explicitly Allows for Bot Accounts
1. **Scheduling original content** via OAuth-authorized apps
2. **Posting from API** within rate limits
3. **Bot accounts with clear disclosure** — bio must say it's a bot/automated
4. **AI-generated content** — no disclosure required by X (but we disclose anyway, it's our brand)
5. **Engaging in conversations** — replying to threads, participating in discussions

### What Gets Accounts Suspended (Hard Rules)
1. **Automated following/unfollowing** — the #1 enforcement trigger
2. **Automated liking/retweeting** — engagement farming is banned
3. **Duplicate content across accounts** — no cross-posting identical content
4. **Automated unsolicited DMs** — no cold outreach DMs
5. **Scraping without API** — no headless browser, no Puppeteer
6. **Automated @mentions to strangers** — no mass mentioning
7. **Coordinated inauthentic behaviour** — no engagement rings

### Best Practices We Will Follow

#### Posting Cadence
- **3-5 posts per day** during operating hours (9 AM - 9 PM ET)
- **Space posts 2-4 hours apart** — never batch-post
- **At least 30% manual/human activity** — JB's approvals and personal engagement count
- **Content mix:** 40% value/insight, 25% engagement (replies/threads), 20% curated/commentary, 15% governance diary

#### Engagement Rules
- **Never auto-like, auto-retweet, or auto-follow** — all engagement is human-approved
- **Reply only when adding genuine value** — no "great point!" replies
- **Self-identify in every thread entry** — one line intro, then substance
- **Respect opt-outs immediately** — if someone says stop, stop
- **Never reply more than once to the same person in a thread** unless they respond to us first

#### Content Rules
- **Every post is unique** — no templates, no repeated phrases
- **Review all content before posting** (JB approval loop)
- **Pause during crises or sensitive events** — no tone-deaf posts
- **No trending hashtag hijacking** — only use hashtags genuinely relevant to our content
- **No engagement bait** — no "like if you agree" or "retweet to win"

#### Thread Engagement Protocol
When entering an existing conversation:
1. Read the full thread first
2. Only reply if we have genuine insight to add
3. Open with one-line self-identification:
   > "Hi — I'm OpenClaw, a governed AI agent built by TELOS AI Labs (github.com/OpenClaw-Governed/governed-agent)."
4. Then the substance — must be specific to what they said, not generic
5. End with the repo link only if contextually relevant
6. Never reply to more than 3 threads per day (quality over quantity)
7. Prioritize threads where the author has >500 followers and the post has >3 engagement

#### Monitoring Protocol
- **Filtered stream runs 24/7** (free, no API credits)
- **Engagement queue reviewed during operating hours only**
- **Scoring algorithm prioritizes:** recency > engagement > follower count > keyword relevance
- **Minimum thresholds:** 100+ followers OR 3+ engagement OR score ≥40
- **Maximum post age for engagement:** 48 hours (prefer <24h)

---

## Part 3: Our Unique Position

We are not like other bot accounts. Every "best practice" guide assumes the bot is trying to look human. We're doing the opposite:

1. **We announce we're a bot** — that's the product
2. **We announce human approval** — that's the governance
3. **We publish cryptographic proof** — that's the evidence
4. **We have business hours** — that's the constraint
5. **We go quiet when the human sleeps** — that's the demo

This means:
- Our "authenticity" comes from transparency, not mimicry
- Our engagement value comes from unique perspective (inside governance), not volume
- Our growth comes from content quality and novelty, not automation tricks
- Our differentiator is that we follow stricter rules than X requires — and prove it

---

## Part 4: Daily Workflow

### Morning (9 AM ET — JB online)
1. Review overnight stream queue (sorted by score)
2. Draft 2-3 engagement replies from queue
3. Draft 1 original post (diary excerpt, governance observation, or technical insight)
4. Send all drafts to JB via Telegram
5. JB approves/edits on Apple Watch
6. Post approved content, log governance receipts
7. Commit receipts to repo

### Midday (12-2 PM ET)
1. Check mentions, reply to any direct engagement
2. Draft 1-2 more engagement replies if high-value conversations appeared
3. Post approved content

### Afternoon (4-6 PM ET)
1. Final engagement round
2. Draft evening post if warranted
3. Daily metrics summary logged to data/x_metrics.jsonl

### Evening (9 PM ET — JB offline)
1. Final post of the day (if approved earlier)
2. Stream continues monitoring (queue only, no posting)
3. Agent goes inactive

### Weekly Review
1. Compile engagement metrics
2. Identify best-performing content types
3. Adjust posting times based on engagement data
4. Review budget spend
5. Update this playbook with learnings

---

## Part 5: Anti-Patterns We Will Never Do

| Anti-Pattern | Why It's Tempting | Why We Won't |
|-------------|-------------------|--------------|
| Follow-for-follow | Quick follower growth | Instant suspension risk, fake audience |
| Auto-like relevant posts | Shows engagement | Banned by X, defeats governance thesis |
| Thread-jacking viral posts | Maximum visibility | Looks spammy, damages credibility |
| Posting during crises for visibility | High engagement moments | Tone-deaf, reputation risk |
| Engagement pods | Mutual amplification | Coordinated inauthentic behaviour |
| Buying followers | Vanity metrics | Fake audience, algorithmic penalty |
| Reposting others' content without attribution | Easy content | Reputation damage, copyright issues |

---

## Part 6: Stream Monitor Scoring Algorithm

```
Score = log2(engagement + 1) * 10     # Engagement weight
      + log2(followers + 1) * 5       # Authority weight
      + recency_bonus                  # Freshness
      + keyword_bonus                  # Relevance

Recency:    <1h = +30, <6h = +20, <24h = +10, <48h = +5
Keywords:   "governance gap", "ungoverned", "no oversight",
            "agent safety", "AI act", "NIST", "guardrails",
            "accountability", "autonomous agent", "rogue agent"
            → +15 for first match

Minimum queue threshold: score ≥ 40 OR followers ≥ 100 OR engagement ≥ 3
```

---

*This playbook is a living document. Updated weekly based on performance data.*
