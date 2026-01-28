# Personal Finance Tracker

A full-stack expense tracker with AI insights. Built it to learn about authentication, caching, and API design while actually solving a problem I had with tracking spending.

[Live Demo](https://financetrackerhasan.vercel.app/) | [GitHub](https://github.com/hasan-ston/FinanceTracker)

## Features

- Expense tracking with categories
- JWT-based authentication
- AI-powered spending analysis using Gemini API
- Automatic monthly summary exports to AWS S3
- Redis caching for fast response times

## Technical Implementation

**API Performance**

Added Redis caching and got an 85% latency drop - from 4ms down to 0.6ms with a 5-minute TTL. Set up cache invalidation on writes so users don't see stale data. Watching those response times drop was honestly pretty satisfying.

**Authentication**

Built JWT authentication from scratch instead of using a library. Learned way more about token generation, expiration, and password hashing by doing it myself. Added refresh tokens to keep users logged in without compromising security too much.

**AI Integration**

Hooked up Gemini API to analyze spending patterns and spit out recommendations. The AI part was easier than expected - most of the work was formatting the data properly. Also set up automatic monthly exports to S3 for keeping records.

**Deployment**

Backend's on Render with PostgreSQL, frontend on Vercel. Split deployment meant dealing with CORS headaches and figuring out environment variables across platforms. Managing secrets properly was more annoying than I thought it'd be, but necessary.

## What I Learned

Caching made a bigger difference than I expected - the performance boost was immediate and noticeable. JWT authentication is straightforward once you understand the flow, but there's a lot of security considerations you don't think about until you implement it yourself. Deploying backend and frontend separately taught me about cross-origin issues the hard way. Working with external APIs like Gemini and S3 showed me how much time you spend on data formatting and error handling versus actual feature code.
