# Professional Profile and Interview Positioning

> **Purpose:** Build a reusable, evidence-based professional profile without
> storing a person's name, contact details, or employer-specific history.

## Profile Design Principles

A strong profile answers four questions quickly:

1. What kind of engineer are you?
2. What systems have you built?
3. What evidence proves the impact?
4. What type of problem do you want to solve next?

Keep the public profile generic. Store personalized stories, metrics, and
employment history in `owner/my_profile.md`.

## Reusable Profile Template

```text
I am a [role] with [experience range] in [two or three core areas].
I have built [representative systems] using [relevant technologies].
My strongest evidence is [measurable result or ownership example].
I am now looking to apply that background to [target problem or role].
```

## Example Backend and AI Profile

> I am a Python-focused backend engineer with experience building APIs,
> microservices, cloud delivery pipelines, and data-intensive applications. I
> have worked across the full delivery lifecycle, from requirements and design
> through testing, deployment, monitoring, and production support. I also have
> experience evaluating LLM and agent workflows for grounding, tool use,
> structured outputs, and safety. I am most effective in roles that combine
> sound software engineering with practical, governed AI integration.

## Sixty-Second Introduction

Use a four-part structure:

- **Present:** current engineering identity.
- **Past:** one or two relevant systems or responsibilities.
- **Proof:** one quantified or observable result.
- **Future:** why the target role is a logical next step.

### Example Introduction

> I am a backend engineer focused on Python, FastAPI, distributed services, and
> production delivery. In recent projects I have designed API contracts,
> integrated PostgreSQL, automated quality and security checks in CI, and
> supported containerized services in cloud environments. I have also evaluated
> retrieval and agent workflows, which taught me to treat grounding, permissions,
> and observability as product requirements. I am looking for a role where I can
> combine those backend fundamentals with responsible AI-enabled services.

## Evidence Inventory

Create an evidence inventory before writing answers. Do not invent metrics; use
an observable outcome when an exact number is unavailable.

|  Capability   |              Evidence prompt              |                      Generic example                      |
| ------------- | ----------------------------------------- | --------------------------------------------------------- |
| Ownership     | What did you initiate and finish?         | Took a security scanner from POC to a CI gate             |
| Reliability   | What failure did you prevent or diagnose? | Added timeouts, retries, and service-level alerts         |
| API design    | What contract decision did you own?       | Preserved older clients with additive schema evolution    |
| Quality       | How did you improve confidence?           | Raised meaningful branch coverage around critical paths   |
| Collaboration | Whose approval or input was needed?       | Aligned product, security, and engineering stakeholders   |
| Scale         | What volume or concurrency mattered?      | Processed records in bounded, restartable batches         |
| AI safety     | What model risk did you control?          | Validated tool arguments and required approval for writes |

## Story Record Format

A machine-readable record makes it easier to reuse a story across interview
questions without changing the facts.

```yaml
story_id: security_scanner_rollout
situation: CI did not include a consistent Python static-security check
task: evaluate a scanner and introduce it without blocking delivery unfairly
actions:
  - built a proof of concept on representative repositories
  - triaged findings by severity and confidence
  - documented justified suppressions with owners and expiry dates
  - obtained product, management, and engineering approval
  - added the scanner to pull-request and release pipelines
result: repeatable security feedback became part of normal delivery
follow_ups:
  - false-positive handling
  - release-blocking policy
  - developer adoption
```

## Tailoring Without Overclaiming

Map each requirement to one of three evidence levels:

|   Level    |              Meaning               |               Interview language                |
| ---------- | ---------------------------------- | ----------------------------------------------- |
| Production | Personally built or operated it    | "I implemented and supported..."                |
| Adjacent   | Worked with it or evaluated it     | "I worked with the team on..."                  |
| Portfolio  | Built outside paid production work | "I implemented a portfolio example to learn..." |

If direct experience is missing, explain the closest transferable pattern and
how you would close the gap. This is stronger than claiming expertise that a
technical follow-up will expose.

## Project Explanation Template

Use this order for a two-minute project walkthrough:

1. Business or operational motivation.
2. System boundary and users.
3. Architecture and data flow.
4. Personal contribution.
5. Difficult trade-off.
6. Testing, security, deployment, and monitoring.
7. Result and lesson.

### Concise Project Example

> A Python team needed security findings earlier in delivery, so I evaluated a
> static-analysis tool against representative services. I built the POC,
> classified true and false positives, and proposed severity-based enforcement
> with documented suppressions. After stakeholder review, I integrated it into
> CI, added developer guidance, and monitored adoption. The project converted an
> informal review concern into a repeatable engineering control.

## Privacy Checklist

Before publishing a profile, search for:

- names, personal email addresses, phone numbers, and street addresses;
- exact interview dates, compensation, recruiter details, and job identifiers;
- private repository owners, customer names, internal hostnames, and secrets;
- confidential production data or unapproved business metrics.

Use the `owner/` directory for personalized preparation, but remember that a
tracked directory is not private merely because it is named `owner`.
