# Manuscript Output Map

## Table 2

- Aggregate source: `derived/benchmark-ph60-ood-mae.csv`
- Rebuilt output: `output/table-2.md`
- Scope: benchmark-configuration PH60 OOD MAE point estimates across seven model families and five GlucoBench datasets.
- Aggregation: the corresponding benchmark evaluation seeds or model seeds are averaged for each model–dataset cell.

## Table 3

- Aggregate source: `derived/clinical-risk-dubosson-ph60-ood.csv`
- Rebuilt output: `output/table-3.md`
- Figure: `output/dts-risk-aggregate.png`
- Scope: completed exported Dubosson PH60 OOD results entering the clinical-safety analysis.
- Aggregation: trajectory MAE and event rates follow each model-specific safety-evaluation sample, while DTS percentages use valid PH60 endpoint pairs. The model-specific endpoint counts can differ.

Table 2 and Table 3 therefore represent distinct analysis samples and aggregation procedures. Their Dubosson MAE entries answer different audit questions: benchmark context in Table 2 and the clinical-safety analysis sample in Table 3.

## Table 4

- Aggregate source: `derived/event-operating-points.csv`
- Rebuilt output: `output/table-4.md`
- Scope: Weinstock OOD warning-policy operating points at PH60 and PH120.

## Table 5

- Aggregate source: `derived/matched-specificity.csv`
- Rebuilt output: `output/table-5.md`
- Figure: `output/matched-specificity-comparison.png`
- Scope: post-hoc specificity-aligned comparison on Weinstock PH60 OOD.

## Table 6

- Aggregate source: `derived/external-transfer.csv`
- Rebuilt output: `output/table-6.md`
- Figure: `output/external-transfer.png`
- Scope: fixed source-model and source-threshold evaluation on ShanghaiT1DM and ShanghaiT2DM.
