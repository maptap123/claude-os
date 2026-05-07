# Marketing Outreach Memory
*Last updated: 2026-05-04*

## Contacts

| Name | Business | Email/Phone | Status | Notes |
| :---- | :---- | :---- | :---- | :---- |

## Key Decisions

- **Research method**: Google Places API via `research_leads.py` (free $200/month credit). Grid-based search covering ~12-mile spacing within target radius.
- **Priority tiers**: TIER_1 = no website (best lead), TIER_2 = has site but weak presence, TIER_3 = decent website (low urgency).
- **First target market**: Tier 2 businesses — dentists, chiropractors, physical therapists, optometrists, auto repair shops, cleaning services, pest control, carpet cleaners. Location: Lawrenceburg, IN + 40-mile radius (covers Cincinnati metro area).
- **Outreach channels**: Email primary (Gmail via MCP), cold calls secondary (from phone numbers in CSV). Facebook/LinkedIn cold messages not reliably automatable.
- **marketing-skills repo**: Corey Haines' open-source marketing skills for AI agents. To be added as git submodule to Marketing Outreach Resources. Key skills: cold-email, seo-audit, ai-seo, revops, sales-enablement, product-marketing-context.
- **Service offering**: Website building + SEO for local businesses. JDC Remodeling (dad's company) is portfolio proof.

## Email Infrastructure (TODO)

- **Domain**: `augmaseo.com` — purchased on Vercel (2026-05-04). DNS managed through Vercel.
- **Google Workspace**: Business Starter plan ($6/month) for custom email (you@yourdomain.com). Keeps everything in Google's ecosystem, works with existing Gmail MCP connection.
- **DNS setup required before sending**: SPF, DKIM, and DMARC records. One-time 30-minute configuration.
- **Warmup required**: 2-3 weeks of gradual volume increase before hitting target sending volume. Tools: Instantly or Warmbox ($0-30).
- **Email verification required**: Run every address through NeverBounce or ZeroBounce (free tiers available) before sending. Anything above 3% bounce rate wrecks sender reputation.

## Planned Sending Ramp-Up

| Week | Emails/day | Cumulative |
|------|-----------|------------|
| 1-2 | Warmup only | 0 |
| 3 | 50/day | 250 |
| 4 | 100/day | 750 |
| 5+ | 200/day | 1,000+ |

## Research Script Status

- `research_leads.py` is built and ready. Needs `GOOGLE_PLACES_API_KEY` env var to run.
- Setup: console.cloud.google.com → create project → enable Places API (New) → create API key → `setx GOOGLE_PLACES_API_KEY "key"`.
- Usage: `python research_leads.py --industry dentist --city "Lawrenceburg, IN" --radius 40`
- Merge: `python research_leads.py --merge *.csv -o master_leads.csv`

## Next Steps (When Returning)

1. ~~Get a domain~~ → **Done.** `augmaseo.com` purchased on Vercel (2026-05-04)
2. ~~Sign up for Google Workspace Business Starter ($6/month)~~ → **Done.** (2026-05-04)
3. Get Google Places API key (free $200/month credit)
4. Run research_leads.py for each target industry
5. Set up DNS records (SPF, DKIM, DMARC)
6. Start domain warmup (2-3 weeks)
7. While warmup runs: qualify the spreadsheet, draft outreach templates
8. Begin sending at 50/day, scale to 200/day
