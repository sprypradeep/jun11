---
id: SPEC-06-01
title: Dashboard UI
status: draft
phase: 6
sequence: 1
dependencies: [SPEC-03-04, SPEC-05-03]
---

# Dashboard UI

## Overview
This specification defines the core user interface for INIVESTEC, focusing on the visualization of the 0–100 Portfolio Health Score, the 5-pillar breakdown, and historical performance. The design must be clean, professional, and instantly comprehensible to reduce "choice paralysis."

## Goals
1. Create a responsive, accessible dashboard layout using Next.js 15 App Router.
2. Visualize the overall Health Score and 5-pillar metrics using intuitive charting libraries.
3. Implement robust data fetching, caching, and loading states using TanStack Query (React Query).

## Requirements

### 6.1 Core Layout & Navigation
- **Layout**: Sidebar navigation (Dashboard, Portfolios, CAS Upload, Settings) and a top bar (User profile, Credit balance, Team switcher).
- **Responsive**: Fully responsive design (mobile, tablet, desktop) using Tailwind CSS.

### 6.2 Portfolio Overview Card (Hero Section)
- **Overall Score**: A large, animated gauge or radial progress bar displaying the 0–100 Health Score. Color-coded (Red: 0-39, Yellow: 40-69, Green: 70-100).
- **Score Change**: Indicator showing the score change vs. the previous month (e.g., "+3.2 pts").
- **Penalty Callouts**: Small, dismissible alert banners if `hhi_penalty` or `fee_drag_penalty` > 0 (e.g., "⚠️ High sector concentration detected").

### 6.3 5-Pillar Radar Chart
- **Visualization**: A radar/spider chart displaying the normalized scores (0-100) for Quality, Value, Momentum, Growth, and Risk.
- **Interactivity**: Hovering over a pillar axis shows the exact score and a brief tooltip explaining the metric.
- **Library**: `recharts` or `@tremor/react` (preferred for fintech aesthetics).

### 6.4 Holdings Table
- **Data**: Paginated table of portfolio holdings.
- **Columns**: Symbol/Name, Quantity, Current Value, Weight (%), Individual Health Score (with color-coded badge).
- **Sorting**: Sortable by Value, Weight, and Health Score.

### 6.5 Historical Score Chart
- **Visualization**: A line chart showing the `overall_health_score` trend over the last 6/12 months (querying the `portfolio_scores` time-series data).
- **Library**: `recharts` (AreaChart).

## Acceptance Criteria
- [ ] Dashboard layout renders correctly on mobile (320px) and desktop (1920px) viewports.
- [ ] TanStack Query successfully fetches and caches portfolio data, showing skeleton loaders during `isPending` state.
- [ ] Radar chart and Area chart render accurately based on mock backend JSON responses.
- [ ] Penalty callouts conditionally render only when backend `portfolio_scores` indicate a penalty > 0.
- [ ] All interactive elements have appropriate ARIA labels for accessibility.

## Out of Scope
- Real-time WebSocket price updates (deferred to Post-MVP).
- Direct trading/execution buttons from the holdings table.

## Technical Details
- **Framework**: Next.js 15 (App Router), React 19, TypeScript.
- **Styling**: Tailwind CSS, `clsx`, `tailwind-merge`.
- **State/Data**: `@tanstack/react-query`, `axios` or native `fetch`.
- **Charts**: `recharts` (lightweight, highly customizable).
