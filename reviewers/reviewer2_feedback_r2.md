# Reviewer 2 Feedback — Round 2

## Summary
The authors have addressed the main methodological concerns raised in the first round. The revised manuscript now explains the nesting of feature selection and cross-validation more clearly, documents the ten-member VotingRegressor ensemble and the meaning of `std_votes`, and distinguishes the different roles of ACE and BOP in the internal and external benchmarks. The lack of a full plain-text external RMSE table remains a limitation of the checked-out repository rather than of the authors' willingness to report it, and the manuscript now states that limitation transparently.

## Major comments
1. The workflow description is now sufficiently explicit to allay the central leakage concern.
2. The clarification of the ensemble construction is useful and materially improves the reproducibility of the manuscript.

## Minor comments
1. If the underlying archived data products are recovered later, I encourage the authors to add the MAE and phase-resolved validation RMSE table as supplementary material.
2. The retained-feature counts for the final best models would still be nice to tabulate in a future polished version, but I do not consider this essential for acceptance of the present draft.

## Recommendation
Accept
