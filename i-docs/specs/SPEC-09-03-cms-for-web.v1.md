---
id: SPEC-09-03
title: Content Management System (CMS) for Web Pages
status: draft
phase: 9
sequence: 3
dependencies: [SPEC-06-01]
---

# Content Management System (CMS) for Web Pages

## Overview
The boilerplate includes static marketing pages. To allow the solopreneur to update FAQs, pricing copy, legal disclaimers, and hero text without redeploying the frontend, this specification introduces a lightweight, database-backed CMS integrated into the admin panel.

## Goals
1. Create a flexible key-value/JSON storage mechanism for site content.
2. Provide an intuitive admin UI to edit and publish content changes.
3. Implement automatic cache invalidation (Next.js ISR) when content is updated.

## Requirements

### 9.1 Database Schema for Content
- Create a `site_content` table:
  - `key` (VARCHAR, PK): e.g., 'hero_title', 'pricing_faq', 'legal_disclaimer_footer'.
  - `value` (JSONB): The actual content (supports strings, arrays, or rich text JSON).
  - `updated_at` (TIMESTAMPTZ).
  - `updated_by` (UUID, FK to users).

### 9.2 Admin CMS API
- **Endpoints**:
  - `GET /api/v1/admin/cms/content`: Fetch all content keys and values.
  - `PUT /api/v1/admin/cms/content/{key}`: Update a specific content key.
- **Validation**: Ensure the updated JSON matches the expected schema for that specific key (e.g., `pricing_faq` must be an array of objects with `question` and `answer`).

### 9.3 Frontend Integration & Cache Invalidation
- **Public Pages**: Update the Next.js public pages (e.g., `/pricing`, `/faq`) to fetch content from the `site_content` API or a dedicated Server Action.
- **Revalidation**: Upon a successful `PUT` request in the admin panel, trigger Next.js `revalidatePath` (via a webhook or direct API call to the frontend) to purge the ISR cache for the affected pages.

## Acceptance Criteria
- [ ] `site_content` table is created and seeded with default values for all marketing keys.
- [ ] Admin CMS UI (`frontend/app/admin/cms/page.tsx`) allows editing of text fields and JSON arrays (for FAQs).
- [ ] Updating a key via the admin UI successfully updates the database and triggers cache revalidation.
- [ ] Public pages reflect the updated content within 60 seconds without a manual server restart.
- [ ] Unit tests verify the JSON schema validation for different content keys.

## Technical Details
- **Frontend**: Use React Hook Form with Zod validation dynamically generated based on the content key's expected schema.
- **Caching**: Leverage Next.js 15 `unstable_cache` or standard ISR with on-demand revalidation tags.
