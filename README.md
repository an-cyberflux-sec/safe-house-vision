Spanish version: README.es.md

# Safe House Vision & Response

## What it is

Safe House Vision & Response — existing cameras → detection → graded alert → evidence with custody → human decides.

## The cascade

Local detection discards almost everything for free; only candidates go up to the verifier (Muse Spark Open via Baseten); only verified becomes an alert. The detector proposes; the verifier and a human decide.

## Loop v1 (Oct 31)

- Clip: safehouse-test-20261028.MOV, SHA-256 D8154A76CCEDCB3F7DC82B60644C1D493FDD757330C810E83754A9882DF5D330.
- Run: runs/run-20261031-120618.jsonl, SHA-256 194F4875A6C6CA7E5D288E936310FE3FBEA5CA94505C9C049FF10B93BB3C0253.
- Detection: 4 s possible_package_theft (0.62), 6 s suspicious behavior (0.85), 10 s package_delivery (0.95).
- Graded alert received on WhatsApp 12:13 PT.
- Measured egress: 6 requests, ~7.3 MB, single destination inference.baseten.co.

## Honest finding

The model labeled as possible theft the staged delivery by the owner himself; the observable facts were correct, the label over-interpreted. That is why there is a verifier and a human.

## Limits

It does not classify people as dangerous by appearance, clothing, or bags; it does not trap or confront. In v1 alert sending is manual; automating it is the next iteration.
