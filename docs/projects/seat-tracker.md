# McMaster Seat Tracker

A course monitoring tool for McMaster students who want to snag seats when they open up.

[Live Site](https://macseats.duckdns.org) | [GitHub](https://github.com/hasan-ston/seatTracker)

## What It Does

Students add courses they're trying to get into, and the system checks Mosaic constantly for availability. The moment a seat opens, it fires off an email so they can register before someone else grabs it.

## Technical Implementation

**Web Scraping & Auth**

Built a Playwright scraper that handles Mosaic authentication and monitors courses. Mosaic uses session-based auth, which meant figuring out cookie management and keeping sessions alive. Not the most exciting problem but necessary to make it work.

**Database Design**

Set up an indexed SQLite database with automatic cleanup jobs. Got queries down to under 10ms using foreign keys and unique constraints to avoid duplicate watches. The schema tracks user registrations, course watches, and notification history.

**Production Deployment**

Deployed on AWS EC2 with Nginx handling the reverse proxy, SSL/TLS, and request buffering. Running Gunicorn with 2 workers for handling concurrent requests, and systemd manages the process and auto-restarts if anything crashes.

This was my first real production deployment. It's been running since launch without major issues, which honestly surprised me given how many things could've gone wrong.

## What I Learned

Deploying a production system end-to-end taught me way more than I expected. Database optimization matters - shaving milliseconds off queries adds up when you're checking hundreds of courses. Nginx configuration was frustrating at first, but understanding reverse proxies and SSL setup made sense once I worked through it. Managing processes with systemd is something I wish I'd learned earlier.

