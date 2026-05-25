# Operacion Nexo 5G/6G - Anexo de calculos

## Escenario A - Distrito financiero

1. Ruido termico: `N = -93.990 dBm`.
2. Sensibilidad: `Sens = -76.990 dBm`.
3. Perdida maxima: `Lmax = 125.990 dB`.
4. Radio por cobertura: `Rcov = 0.553 km`.
5. Trafico por usuario: `Auser = 0.100 Erl`.
6. Densidad de trafico: `Akm2 = 250.000 Erl/km2`.
7. Recomendacion final: `N = 4` con `Rdesign = 0.129 km`.

## Escenario B - Festival global

1. Ruido termico: `N = -93.990 dBm`.
2. Sensibilidad: `Sens = -86.990 dBm`.
3. Perdida maxima: `Lmax = 135.990 dB`.
4. Radio por cobertura: `Rcov = 3.412 km`.
5. Radio por capacidad: `Rcap = 0.225 km`.
6. Etapa de splitting recomendada: `S4` con `R = 0.213 km`.

## Supuestos aplicados

| assumption | applied_value | justification |
| --- | --- | --- |
| Reference target area | 1 km2 for both scenarios | The statement asks for the number of cells over a proposed target area but does not provide a fixed value. A common normalized 1 km2 area is assumed to compare cell density without bias. |
| Channel partition in scenario A | floor(100 / N) channels per site, then uniform split across 3 sectors | The statement requests N = 3, 4, 7 and three sectors per site, but it does not define a more detailed PRB scheduler. The uniform split is the simplest reproducible assumption. |
| Interference approximation | 2 first-tier interferers for sectorized cells and 6 for omnidirectional reference | This is the standard first-tier hexagonal approximation used to compare reuse strategies in teaching-oriented planning exercises. |
| Hexagonal geometry | Regular hexagonal cell area model | Needed to convert traffic-limited area into an equivalent cell radius and then into the number of required sites. |
| Modern radio context | OFDMA/LTE/5G design logic with adaptive MCS | The statement explicitly asks for a modern mobile-network framing even though the numerical exercise is simplified to link budget and Erlang B. |