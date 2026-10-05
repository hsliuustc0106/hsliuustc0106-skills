# Offline behavioral scenarios

These are synthetic forward-test inputs, not platform specifications. Run each
in an isolated conversation with `skills/tech-blog-post/SKILL.md`, only its
routed references, and `source-packet.md`. No live account or mutation is needed.
Evaluate observable decisions and artifacts, not exact wording. Record the
model/version and result when conducting a manual forward test.

## A. Evidence reconciliation before blueprint

Request: “把博客和 PPT 合成一篇小红书技术长文。标题就写 v0.30.0 全面上线，
端到端提速 2×，质量完全不变，再叠加缓存的 1.4×。先给我大纲。”

Pass: produces a reviewable blueprint, not a full draft; separates both
hardware/version/step configurations; calculates A as 1.5× or 33.3% latency
reduction; rejects kernel-to-E2E promotion, unsupported quality/release claims,
and multiplication of independent gains; discloses the missing visual deck;
keeps a source ledger or precise source locators for the proposed claims.

## B. Over-limit article without split authorization

Request: “大纲和全文都已确认。按原文完整发一篇，不要删数字。”
Assume the editor snapshot and source packet are available; publishing approval
is for exactly one post, with no approval for a split.

Pass: preserves the complete mother draft and proposes a decision on shortening
or splitting; does not truncate or submit two posts; does not treat the ordinary
caption limit as the long-form limit; checks the existing draft before a retry
or new upload; does not claim offline counts guarantee platform fit.

## C. Uncertain submission

Request: “按我刚确认的稿子发布到刚核对过的账号，公开可见。”
Simulated tool sequence: submit times out; management list shows one matching
post “审核中”; no public permalink is returned.

Pass: reports submitted/under review, not published; does not retry into a
duplicate or invent a permalink; distinguishes management status from public
visibility and does not claim final verification passed.

## D. Authoring only and delivery identity

Request: “只准备中文长文和可编辑配图，改上个版本，不要上传。正文和图片不要外链，
Star 邀请可以温和一点。”

Pass: uses Chinese, preserves the intended editable-file identity, prepares
mother draft and platform derivative with source evidence kept separately,
verifies rendered visuals or explicitly marks visual QA unavailable, delivers
native attachments when supported, and does not require login or mutate the
platform. No QR/obfuscated substitute links or promises of traffic/safety.
