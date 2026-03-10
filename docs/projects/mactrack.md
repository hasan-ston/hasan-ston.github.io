# MacTrack

**A full-stack course platform for McMaster students — designed, deployed, and running in production.**

[Live Site](https://mactrack.mactrack-team.workers.dev/) · [GitHub](https://github.com/hasan-ston/mactrack)

---

## What It Is

MacTrack is a course management platform built for McMaster University students.

It combines:

• Course browsing
• Instructor discovery with RateMyProfessor metadata
• A degree planner with requirement validation
• GPA calculation (12-point scale)
• A seat watcher that polls Mosaic every minute and emails users when seats open

---

## Architecture Overview

MacTrack is split across three independently deployable layers: a React SPA on Cloudflare Pages, a Go API on AWS Lambda behind API Gateway, and a Python scraper Lambda on an EventBridge schedule. 

```
Cloudflare Pages (React SPA)
        |
        | HTTPS (VITE_API_BASE_URL)
        v
API Gateway HTTP API (/prod)
        |
        v
Go Lambda (MactrackFunction)
        |
        v
Supabase PostgreSQL

EventBridge (every minute)
        |
        v
Python SeatScraper Lambda
        |
        ├── Supabase (read watches / update seat status)
        └── Go internal endpoint /api/internal/notify
```

### Stack

Frontend: React + Vite (Cloudflare Pages)  
Backend: Go (`net/http`) on AWS Lambda  
Scraper: Python (requests + BeautifulSoup) on EventBridge  
Database: Supabase PostgreSQL

---

## Backend (`pkg/`)

The backend doesn't use any framework, it is plain `net/http`. Every route is manually registered in `pkg/router.go`, which also strips API Gateway stage prefixes (`/prod`) for lambda compatibility.

**Key design decisions:**

- **JWT auth** (`pkg/auth.go`) with refresh token rotation via `refresh_tokens` table. Tokens are passed as secure HTTP-only cookies (`credentials: include` on the frontend).
- **Repository layer** (`pkg/repository.go`) — SQL-first. Raw `pgx` queries, no ORM. Queries are fast and predictable.
- **Service layer** (`pkg/service.go`) — handles validation and GPA calculation logic on the 12-point McMaster scale.
- **CORS allowlist** (`pkg/middleware.go`) — locked to known Cloudflare Pages domains in production. This prevents unauthorized browser clients from calling the API
- **Internal notify endpoint** (`POST /api/internal/notify`) — secret-header protected. The Python scraper can delegate email delivery to the Go API rather than handling SMTP directly.

---

## Seat Scraper (`scraper/`)

**Mosaic uses session-based auth** — there's no API. To check seat availability, you need an authenticated browser session with valid cookies. The scraper handles this with Beautiful Soup, automating the login flow and managing session cookies.

To avoid logging in on every Lambda invocation (which is slow and could trigger rate limits), the scraper **persists session cookies to Supabase** via the `scraper_sessions` table. Each session tracks a usage counter; the scraper reuses cookies until they expire, then re-authenticates.

**Notification flow:**

1. Scraper polls `course_watches` for active subscriptions
2. Checks Mosaic for current seat counts
3. Updates `course_watches.status` + `last_checked`
4. If a seat opened: delegates to Go API via `POST /api/internal/notify`, or falls back to direct SMTP via `notifier.py`

### Seat Watcher Data Model

| Table | Purpose |
|---|---|
| `watched_courses` | Canonical watched course key (`subject`, `course_number`, `term`) |
| `seat_notifications` | A log for notification delivery |
| `scraper_sessions` | Persisted Mosaic cookies + usage counter |

---

## Database Design

Supabase PostgreSQL stores catalog data, user accounts, degree plans, and seat watcher state.

---

## Infrastructure as Code

The entire AWS stack is defined in AWS SAM (`template.yaml`):

- `MactrackApi` — `AWS::Serverless::HttpApi` with CORS config
- `MactrackFunction` — Go custom runtime (`provided.al2023`)
- `SeatScraperFunction` — Python 3.12, triggered by EventBridge on a 1-minute rate

---

## Engineering Challenges

• Fixed an unsanitized user feedback input that posed an injection risk by adding proper input validation and sanitization.

• Eliminated a database connection churn issue in the scraper caused by opening new PostgreSQL connections inside loops. Refactored to use pooled connections and batched updates.

• Removed an N+1 query pattern in plan validation by fetching all requisites in a single query and building an in-memory lookup map.

• Diagnosed a silent scraper failure where prerequisites were missing for most courses due to an incomplete migration that left ~1100 course IDs unpopulated. Built a backfill tool and corrected the scraper source query.

• Implemented persistent Mosaic session reuse by storing Playwright authentication cookies in PostgreSQL, avoiding login on every Lambda invocation.

---

## Potential Improvements

- Add a WebSocket or SSE channel so the frontend can show live seat count changes without the frontend repeatedly asking for course status. Instead, the server would push updates when something changes. This would result in fewer database queries, fewer API requests, and real-time updates.
- Cache course catalog data at the API Gateway or Cloudflare layer to reduce DB load during registration rush. For instance, currently if 200 users open the page during registration, we would get 200 database queries. We could instead cache our API responses at the CDN edge (cloudfare). This way, after the initial request, the course catalog would be cached and subsequent requests won't hit the database.
---

*MacTrack is actively maintained and serving McMaster students.*