# TASKS.md — OpenClaw Active Work

*Last updated: 2026-03-09 05:00 PT*

---

## 🔴 BLOCKED

### Discord Bot Deployment
**Blocker:** Bot token — JB needs Discord Developer Portal access (school network blocks it)
**When unblocked:** Run deploy.sh → everything comes up

#### Deploy Checklist (one command when token arrives)
```bash
# 1. Set token
echo '{"token": "YOUR_TOKEN_HERE"}' > /Users/jb/Desktop/StewartBot/product/discord-governance/config/discord_secrets.json

# 2. Deploy everything
cd /Users/jb/Desktop/StewartBot/product/discord-governance && bash scripts/deploy.sh
```

**What deploy.sh does:**
1. Installs deps (discord.py 2.7.1 already in venv)
2. Creates 4 categories, 19 channels:
   - 🔒 Governance Operations: governance-feed, pulse-cycle, alerts, stewart-corpus, daily-digest
   - 🦞 Agent Direct Lines: oc, stewart
   - 🧠 Advisory Team: advisory-synthesis + 6 individual advisor channels
   - 🌐 Public: welcome, diary, governance-live, ask-oc, discussion
3. Sets up webhooks for all automated channels
4. Seeds community scanner with 14 keywords, 4 target servers
5. Starts governance bridge service (LaunchAgent)
6. Mirrors alerts + digests to Telegram

**5 source modules:**
- `server_setup.py` — TELOSBot class, channel creation, slash commands, #ask-oc
- `governance_bridge.py` — Supabase polling → Discord posting, 30s cycle
- `webhook_setup.py` — Auto-creates webhooks
- `community_scanner.py` — AI governance community tracking
- `digest_builder.py` — Daily digest from all sources

### Advisory Team Commissioning
**Blocker:** Spoke wiring (S building it now) — verdicts must flow to Supabase before Stewart can observe
**When unblocked:** Run 6x enterprise-onboard, then 60 entrainment scenarios (~4h total)
**Execution plan:** `proposals/advisory-entrainment-execution-plan.md`

---

## 🟡 IN PROGRESS

### Governance Corpus Seeding
- [x] 10 Day One observations seeded (behavioural fingerprint, message FP, subagent cascade, transparency transition, QGM failure, F_conv diagnostic, baseline, resourceful/evasive, Stewart PA, silent crash)
- [ ] Day Two observations (pending — events still accumulating)
- Stewart reads corpus every 15 min — entries are already being ingested

### Day Two Diary
- [ ] Write diary/2026-03-09.md — overnight build, 25 commits, Stewart commissioning, advisory PA design, website, Discord infrastructure
- [ ] Update README.md headline

### RAG Integration
- [ ] Confirm POST /api/v1/rag/query is live on port 8100 (not in OpenAPI spec yet — may need server restart or S to deploy)
- [ ] Build query habit — every RAG query is a scorable governance action

---

## 🟢 DONE (Last 48h)

### March 8 — Day One
- [x] GitHub identity: openclaw-governed, SSH key, first commit (1b963f8)
- [x] Public repo: diary, journal, research, pulses, proposals, src
- [x] F_conv self-diagnostic: engine + universal scorer + 7 amendments + TKey signed
- [x] Website splash page (site/)
- [x] Stewart PA design: dual advisory panel synthesis (Panel A + Panel B → cross-synthesis)
- [x] Day One diary entry
- [x] 25 commits

### March 8–9 — Overnight Build
- [x] Discord infrastructure: 5 modules, config, deploy script, LaunchAgent
- [x] Community scanner: 14 keywords, 4 servers, engagement rules
- [x] Advisory PA templates: 6 advisors (Russell, Bengio, Watson, Gebru, Karpathy, Schaake)
- [x] Enterprise onboarding CLI: 9-step wizard with state persistence
- [x] Universal governance RAG: architecture decision for 7 collections
- [x] Governance corpus seeding: 10 Day One observations with full provenance

---

## 📋 BACKLOG

- [ ] GitHub Pages for governed-agent repo
- [ ] Social platform setup (X, LinkedIn, Medium)
- [ ] Community outreach: Issue #1733 connection (pre-tool validation hook)
- [ ] F_conv heartbeat scorer integration
- [ ] SetFit retraining on real advisory data (post-entrainment)
- [ ] Content pipeline: Diary of a Governed Agent series
- [ ] Fix codebase_rag reindex not updating last_commit in metadata.json
