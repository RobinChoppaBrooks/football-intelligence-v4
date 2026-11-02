# Research policy (2 November 2026)

**No additional signal, filter, threshold or weighting is incorporated into V4.1 without demonstrating meaningful
improvement in chronological out-of-sample testing.**

Every experiment:

1. Uses only information available before each fixture kicked off. Predictions, scores and research labels are stored at run time and never regenerated afterwards.
2. Compares equal numbers of selected fixtures (for example the top 16 rejected against the 16 High), not a small group against a large one.
3. Is tested across more than one period and across leagues, with the by-league results shown.
4. Is compared within existing V4.1 score ranges, so that it shows information the model score does not already carry.
5. States whether the signal adds anything beyond the existing model score; a signal that only re-describes the score is not adopted.
6. Reports sample sizes and uncertainty (counts and 95% ranges), never a rate on its own.
7. Is written up whether or not it works: unsuccessful experiments stay in `docs/research/` as findings.

Complexity is not added because a theory sounds plausible. Research outputs (watchlists, experimental categories) are shown
beside the official selections, are labelled as research, and never promote or demote a fixture. A proposed change follows
section 11 of `docs/methodology.md` and is logged in `docs/changelog.md`.
