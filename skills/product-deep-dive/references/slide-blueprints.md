# Product deep-dive slide blueprints

Use these as a starting composition. Adapt the emphasis to the product and the
audience. The research questions guide investigation; they are not mandatory
boxes to fill with weak evidence. The default visual system comes from
[template-style.md](template-style.md); a current task's template takes priority.

## Slide 1: Business — why this product matters

**Audience test:** Can a reader explain who would choose this product, for what
job, against which alternative, and with what commercial caveat?

| Region | Content | Suggested treatment |
| --- | --- | --- |
| Header | Product/vendor, category, as-of date; a specific takeaway about its value | Short takeaway title and identity line |
| Left, about 56% of body width | One concrete workflow showing what changes for the user | Large sourced product screenshot or before/after flow, with a short caption |
| Right, about 42%, separated by a gutter | User/buyer and job; value and differentiation; pricing/distribution; adoption evidence and business risk | Up to four numbered findings, each with a blue heading and about two lines of explanation |
| Bottom strip | Best-fit use case and the main business risk or unresolved question | One sentence, qualified as an assessment where appropriate |
| Footer | Short source references matching claim markers | Linked source titles; full details in notes/ledger |

Choose the commercial facts that explain adoption: distribution, purchasing
friction, switching costs, ecosystem fit, or value capture. Do not force all of
them onto the page. A logo wall or funding figure alone does not show product
success. If comparing alternatives, use at most a few decision-relevant
dimensions and make the comparison scope explicit.

Good takeaway pattern: **“[Product] helps [specific user] accomplish [job] through
[differentiator], with [important adoption constraint].”** Replace every slot with
evidence-backed content. A title such as “Product overview” carries no finding.

## Slide 2: Technical — what enables the value

**Audience test:** Can a reader trace a real task through the system, identify
what is distinctive, and name the main technical constraint?

| Region | Content | Suggested treatment |
| --- | --- | --- |
| Header | A takeaway connecting a mechanism to its benefit and tradeoff | Claim title, consistent identity/date treatment |
| Left, about 56% of body width | The same use case, traced from input through documented components to output | Large editable architecture or sequence diagram, typically four to six major nodes |
| Right, about 42%, separated by a gutter | Distinctive mechanisms, execution/dependencies, outputs or verification, and the main constraint | Up to four numbered findings; connect each design choice to its benefit or tradeoff |
| Bottom strip | Most consequential integration/deployment limit, evidence gap, or next verification | One concise statement |
| Footer | Technical evidence supporting nodes, arrows, and claims | Linked docs, paper sections, or pinned code references |

Label what crosses each important boundary: data, requests, tool calls, control,
or physical signals. Show third-party dependencies and human intervention when
they change the behavior. Keep inference visually distinct with a text label or
legend; color alone is insufficient. Do not turn a capability diagram into an
assertion about undocumented server-side architecture.

Select technical details for explanatory value:

- For software or AI: runtime flow, model/tool dependencies, data and state,
  integrations, permissions, deployment, and failure behavior when documented.
- For hardware: major subsystems, signal/power/material flow, interfaces,
  operating envelope, and physical constraints when documented.
- For other products: the process and dependencies that create the user outcome.

Use a sourced benchmark or specification only when it helps explain the main
claim; retain units, conditions, and attribution. Do not add a chart merely to
make the slide look quantitative.

Good takeaway pattern: **“[Documented mechanism] enables [business-slide benefit],
while [dependency or constraint] limits [relevant use case].”** If the mechanism
is not disclosed, explain the known interfaces and make that gap explicit.

## Density and visual guidance

- Use the default template's 960 × 540 pt canvas, approximately 42 pt horizontal
  margins, and measured content bands. Keep the left visual dominant. A supplied
  template overrides these measurements.
- Aim for roughly 120–180 English words per slide, excluding source notes; use
  visual fit and reading effort for other languages. This is a drafting guide,
  not a quota. Diagrams and screenshots need their own breathing room.
- Preserve the reference hierarchy: Arial 30 pt title, 16 pt subtitle, 17 pt
  numbered headings, 14 pt body, and 15 pt takeaway. Caption and source styles
  are specified separately in the style reference. Do not shrink body text below
  the reference size; remove secondary points or simplify the composition.
- Keep full URLs and detailed provenance in notes or the ledger, with compact
  clickable references on the slide. Put substantive caveats in readable body text.
- Use a shared palette and recurring terms across the two slides. Draw attention
  to the finding, the explanatory visual, and the caveat in that reading order.

## When explicitly limited to one slide

Use one takeaway header, a business summary on the left, a compact technical flow
on the right, and a shared limitation/source strip below. Retain the target user,
job, differentiator, enabling mechanism, and main constraint. Move commercial and
implementation detail into notes. Do not silently add a second slide.
