---
id: SPEC-07-03
title: White-Label Reports
status: draft
phase: 7
sequence: 3
dependencies: [SPEC-05-03, SPEC-07-02]
---

# White-Label Reports

## Overview
This specification defines the asynchronous generation and delivery of branded PDF reports summarizing a client's Portfolio Health Score and AI narrative. This is a core value proposition for the B2B AdvisorOS, allowing firms to present INIVESTEC insights under their own brand.

## Goals
1. Generate professional, branded PDF reports containing portfolio metrics, charts, and AI narratives.
2. Allow advisory firms to customize the report with their logo and brand color.
3. Deliver the generated report via email (Resend) or provide a secure download link.

## Requirements

### 8.1 Branding Configuration
- Extend the `teams` table (or a related `team_settings` table) to include `brand_logo_url` (string) and `brand_color_hex` (string, default: scaffold's green).
- These settings are injected into the PDF template during generation.

### 8.2 PDF Generation Engine
- **Library**: `WeasyPrint` (Python) or `@react-pdf/renderer` (Next.js). *Preference: WeasyPrint for easier server-side HTML/CSS to PDF conversion with dynamic data.*
- **Template**: An HTML template (`backend/app/templates/report.html`) styled with Tailwind-like utility classes (via inline CSS or WeasyPrint-compatible CSS) containing:
  - Firm Logo and Brand Color header.
  - Client Name (anonymized/generic if PII rules dictate, or explicit if consented) and Report Date.
  - Overall Health Score (large gauge representation).
  - 5-Pillar breakdown table.
  - AI Narrative (Summary, Strengths, Risks, Actions).
  - Standardized financial disclaimer footer.

### 8.3 Asynchronous Task & Delivery
- **Endpoint**: `POST /api/v1/advisor/reports/generate` (Payload: `portfolio_id`, `delivery_method`: 'email' | 'download_link').
- **Taskiq Job**: `generate_and_send_report(task_id, portfolio_id, team_id, delivery_method)`.
  1. Fetch portfolio scores and the latest cached AI narrative (SPEC-05-03).
  2. Fetch team branding settings.
  3. Render HTML template.
  4. Convert to PDF using WeasyPrint.
  5. If `email`: Upload PDF to secure storage (or encode as base64 if small) and send via Resend (`backend/app/services/email/resend_service.py`).
  6. If `download_link`: Store PDF temporarily and return a signed, time-limited (24h) download URL.

## Acceptance Criteria
- [ ] `team_settings` schema and API endpoints for updating `brand_logo_url` and `brand_color_hex` are implemented.
- [ ] WeasyPrint successfully converts the HTML template to a high-quality PDF, correctly rendering the dynamic brand color and logo.
- [ ] Taskiq job handles the end-to-end generation and Resend email delivery without blocking the main thread.
- [ ] Generated PDFs include the mandatory financial disclaimer footer.
- [ ] Unit tests mock WeasyPrint and Resend to verify the task logic and payload construction.

## Out of Scope
- Interactive PDFs (e.g., clickable charts). Charts will be rendered as static images or CSS-based bar gauges in the PDF.
- Multi-language PDF generation (deferred to Post-MVP).

## Technical Details
- **Libraries**: `weasyprint`, `jinja2` (for HTML templating), `resend` (scaffold integration).
- **Performance**: PDF generation is CPU-intensive. The Taskiq worker handling this must have a generous timeout (e.g., 60s) and be isolated from the main API workers.
