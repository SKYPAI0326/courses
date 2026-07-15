# Dedup Scan: office-ai

## Reviewer verdict

- Baseline lint: 20 pages, BLOCKER 0, ERROR 0, WARN 0.
- `MAJOR / CONTENT_THIN / LEARNER_PATH`: 11 pages fully demonstrate an artifact in section (03), then repeat the same material, artifact, and operating path as `Together` in section (06).
- `MINOR / Shared Copy`: the complete paragraph labelled `帶著走的一句話` appears on 9 pages. It is instructional framing, not navigation or a required warning.

## Activity Identity Audit

| page | Demo material / artifact | repeated Together | overlap verdict | action |
|---|---|---|---|---|
| ch1/CH1-3.html | first conversation / office capability answer and meeting notice | reopens a chat and regenerates the same outputs | 3+ fields identical, MAJOR | retain the first run; section (06) keeps only transfer Solo and completion evidence |
| ch2/CH2-1.html | Mid-Autumn client email / controlled email | reruns baseline, role, example, and controlled version | 3+ fields identical, MAJOR | retain first run; keep customer-service Solo |
| ch2/CH2-3.html | complaint email / three-round controlled reply | recreates the same three rounds | 3+ fields identical, MAJOR | retain first run; keep negotiation Solo |
| ch3/CH3-1.html | work log / controlled weekly report | recreates weak, controlled, and repair versions | 3+ fields identical, MAJOR | retain first run; keep status-word Solo |
| ch3/CH3-2.html | expense details / cleaned table | reruns the same cleanup and verification | 3+ fields identical, MAJOR | retain first run; keep deduplication-decision Solo |
| ch3/CH3-3.html | project update / sourced summary | reruns the same weak and controlled summaries | 3+ fields identical, MAJOR | retain first run; keep manager-summary Solo |
| ch4/CH4-1.html | incomplete product facts / slide outline | rebuilds weak and controlled outlines | 3+ fields identical, MAJOR | retain first run; keep alternate-product Solo |
| ch4/CH4-2.html | slide outline / expanded slide copy | rebuilds weak and controlled slide copy | 3+ fields identical, MAJOR | retain first run; keep pricing-slide Solo |
| ch4/CH4-3.html | slide copy / image brief and search terms | rebuilds the same brief and terms | 3+ fields identical, MAJOR | retain first run; keep another-slide Solo |
| ch5/CH5-2.html | Q2 transcript / three-zone meeting record | recreates weak and controlled records | 3+ fields identical, MAJOR | retain first run; keep project-meeting Solo |
| ch5/CH5-3.html | meeting transcript / next-meeting notice | regenerates weak and controlled notice | 3+ fields identical, MAJOR | retain first run; keep registration-reminder Solo |

## Shared Copy Audit

| repeated copy | pages | allowed reason | action |
|---|---:|---|---|
| `帶著走的一句話` full paragraph | 9 | useful only as course framing and closure | retain CH1-1 and CH6-3; remove from CH1-2, CH1-3, CH1-4, CH2-1, CH2-2, CH6-1, CH6-2 |
