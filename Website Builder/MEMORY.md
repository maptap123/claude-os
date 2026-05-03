Source: Cowork Toolkit by Jeff Su — [coworkacademy.ai/toolkit](https://coworkacademy.ai/toolkit)

# Website Builder Memory

*Last updated: 2026-05-01*

## Contacts

*People relevant to the JDC website — designers, devs, SEO vendors, etc. Populated as we work.*

- *(none yet)*

## Site Info

| Detail | Value |
| :---- | :---- |
| GitHub repo | https://github.com/maptap123/jdc-website (private) |
| Local files | C:\Users\mapta\Documents\Claude OS\Website Builder\Website\ |
| Framework / tech | Vanilla HTML/CSS/JS. Tailwind CDN on remodeling.html only (inconsistent). Images on Cloudinary. |
| Local dev | `node serve.mjs` → localhost:3000. Screenshots via `node screenshot.mjs`. |
| Pages | index.html, about.html, custom-home.html, custom-home-portfolio.html, remodeling.html, remodeling-bathroom.html, remodeling-kitchen.html, remodeling-whole-home.html, remodeling-addition.html, quote.html, articles.html, articles/how-long-does-a-kitchen-remodel-take.html, articles/how-to-choose-a-custom-home-builder.html, articles/how-long-does-a-bathroom-remodel-take.html, portfolio-caudill.html, portfolio-cameron.html, portfolio-larkin.html, portfolio-alice.html, portfolio-cleeter.html, portfolio-drouge.html, portfolio-perfect.html |

## Company Details

| Detail | Value |
| :---- | :---- |
| Company name | JDC Construction |
| Location | Lawrenceburg, Indiana / Southeast Indiana |
| Founded | 1996 |
| Owners | Jason & Lisa Cox |
| Phone | (812) 637-2684 |
| Email | info@jdcconstruction.com |
| Award | Indiana Remodeler of the Year, 2019 (Indiana Builders Association) |
| NAHB Designations | GMR, GMB, CGR, CAPS, CGP |
| Brand colors | Navy #091b37, Gold #f2b900, Cream #f7f5f2 |
| Fonts | Cormorant Garamond (display serif) + DM Sans (body sans) |

## Blog / Articles

| Detail | Value |
| :---- | :---- |
| Index page | articles.html |
| Article folder | articles/ |
| Keyword files | Custom Home Keywords.csv, Remodel Keywords.csv |
| Article image source | Pexels CDN + Cloudinary |
| Coming soon | (none — all planned articles are published) |

### Automation

| Detail | Value |
| :---- | :---- |
| Prompt file | Website/blog-automation-prompt.md (in git repo) |
| Article tracker | Website/published-articles.md (in git repo) |
| Template | Website/articles/_TEMPLATE.html (in git repo) |
| Schedule | Weekly, Monday 9:07 AM Eastern (13:07 UTC, cron: `7 13 * * 1`) via remote agent |
| Remote agent | Routines dashboard: https://claude.ai/code/routines |
| Last run | Not yet run |

Note: The remote agent runs from the git repo at `https://github.com/maptap123/jdc-website`. All automation files live there so the agent can access them.

### Published Articles

| Article | File | Primary Keyword | KD | Vol | Cluster Keywords Used |
| :---- | :---- | :---- | :---- | :---- | :---- |
| How Long Does a Kitchen Remodel Take? | articles/how-long-does-a-kitchen-remodel-take.html | how long does a kitchen remodel take | 18 | 880 | kitchen remodel timeline, Dearborn County, SE Indiana, Lawrenceburg |
| How to Choose a Custom Home Builder | articles/how-to-choose-a-custom-home-builder.html | how to choose a custom home builder | 0 | 170 | custom home builder near me, custom home builders, how long does it take to build a custom home, how much does it cost to build a custom home, SE Indiana, Cincinnati, Dearborn County |
| How Long Does a Bathroom Remodel Take? | articles/how-long-does-a-bathroom-remodel-take.html | how long does a bathroom remodel take | 4 | 880 | how to plan a bathroom remodel, do you need a permit for bathroom remodel, small bathroom remodel, bathroom remodel cincinnati, cincinnati bathroom remodel, SE Indiana, Dearborn County |
| How Much Does a Kitchen Remodel Cost? | articles/how-much-does-a-kitchen-remodel-cost.html | how much does a kitchen remodel cost | 33 | 4400 | kitchen remodel cost, how much does it cost to remodel a kitchen, SE Indiana, Dearborn County, Lawrenceburg |
| Home Addition Cost: What to Expect in 2026 | articles/home-addition-cost-2026.html | home addition cost | 20 | 1000 | how much does a home addition cost, home addition cost 2026, house addition cost, Dearborn County, Cincinnati, SE Indiana |
| How to Remodel a Bathroom: A Step-by-Step Guide | articles/how-to-remodel-a-bathroom.html | how to remodel a bathroom | 40 | 1900 | bathroom remodel step by step, how to remodel a bathroom, Southeast Indiana, Dearborn County, Lawrenceburg, Cincinnati tri-state area |

## Mobile Audit (2026-05-01)

*Full audit of mobile look & feel across all key pages.*

### Critical
- Landing page (index.html) has no nav — no `components.js`, no hamburger, just the two clickable panels
- Hero sections take `100vh; min-height: 700px` with scroll indicator hidden on mobile → no scroll cue, looks like a dead end
- Button text drops to `0.65rem` (10.4px) on mobile — too small for touch, especially ghost button with low-contrast border
- Section eyebrow labels at `0.62rem` (9.9px) with `0.3em` letter-spacing — illegible on phone

### Moderate
- Footer contact info at `rgba(255,255,255,0.38)` — phone and email are nearly invisible
- Gallery images use fixed 240px height on mobile instead of aspect-ratio — wide exterior shots and tall interiors get same crop
- Section padding `4rem` (64px) top/bottom on mobile creates excessive dead space
- Landing panels force all hover content visible simultaneously — 4 buttons + 2 descriptions competing in bottom half of screen
- No `:active` states on any interactive elements — no tap feedback on mobile

### Minor
- Mobile nav overlay links have no tap padding — missed tap closes the overlay
- Stats grid 2x2 borders get visually noisy on mobile
- About page accent image hidden on mobile — loses the layered editorial feel

### Top 5 Fixes (priority order)
1. Add mobile nav to landing page
2. Reduce hero height on mobile (min-height: 80dvh or 500px) + restore subtle scroll indicator
3. Bump minimum text sizes: 0.75rem floor for buttons, 0.7rem for labels, increase footer contrast
4. Use aspect-ratio for gallery images instead of fixed 240px height
5. Add `:active` states to all buttons and links for tap feedback

## Current Priorities

*What we're actively working on. Update as tasks are completed or reprioritized.*

- [x] MOBILE: Add nav to landing page (index.html) ✓ 2026-05-01
- [x] MOBILE: Reduce hero height on interior pages + add scroll cue ✓ 2026-05-01
- [x] MOBILE: Bump minimum text sizes and footer contrast ✓ 2026-05-01
- [x] MOBILE: Replace fixed gallery heights with aspect-ratio ✓ 2026-05-01
- [x] MOBILE: Add :active states for tap feedback ✓ 2026-05-01
- [ ] SEO: Add meta descriptions to all pages
- [ ] SEO: Update title tags with local geo keywords
- [ ] SEO: Add structured data (LocalBusiness schema)
- [ ] Design: Make CSS approach consistent (drop Tailwind CDN from remodeling.html)
- [ ] Design: Add testimonials/reviews section
- [ ] Content: Update copyright year (still shows 2024)
- [ ] Technical: Add favicon, sitemap.xml, robots.txt

## Key Decisions

*Design, SEO, or technical decisions made during sessions. Record reasoning so future sessions don't re-litigate them.*

- *(none yet)*
