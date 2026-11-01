# Safe House Vision & Response

## Qué es

Safe House Vision & Response — cámaras existentes → detección → alerta graduada → evidencia con custodia → humano decide.

## La cascada

La detección local descarta casi todo gratis; solo los candidatos suben al verificador (Muse Spark Open vía Baseten); solo lo verificado se vuelve alerta. El detector propone; el verificador y un humano deciden.

## Loop v1 (31-oct)

- Clip: safehouse-test-20261028.MOV, SHA-256 D8154A76CCEDCB3F7DC82B60644C1D493FDD757330C810E83754A9882DF5D330.
- Corrida: runs/run-20261031-120618.jsonl, SHA-256 194F4875A6C6CA7E5D288E936310FE3FBEA5CA94505C9C049FF10B93BB3C0253.
- Detección: 4 s possible_package_theft (0.62), 6 s suspicious behavior (0.85), 10 s package_delivery (0.95).
- Alerta graduada recibida en WhatsApp 12:13 PT.
- Egreso medido: 6 requests, ~7.3 MB, destino único inference.baseten.co.

## Hallazgo honesto

El modelo etiquetó como posible robo la entrega simulada por el propio dueño; los hechos observables eran correctos, la etiqueta sobre-interpretó. Por eso hay verificador y humano.

## Límites

No clasifica personas como peligrosas por apariencia, ropa o bolsos; no atrapa ni confronta. En v1 el envío de la alerta es manual; automatizarlo es la siguiente iteración.
