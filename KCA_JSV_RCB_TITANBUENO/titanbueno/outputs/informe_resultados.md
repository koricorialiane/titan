# Operacion Nexo 5G/6G - Informe tecnico

## Resumen

Este informe desarrolla el reto Operacion Nexo 5G/6G para Nueva Pangea comparando dos escenarios de alta demanda: un distrito financiero urbano y un festival masivo temporal.
El escenario A queda limitado por capacidad y recomienda N=4; el escenario B queda claramente limitado por densidad y exige cell splitting hasta la etapa S4.

## 1. Introduccion

El problema de una red movil moderna no se resuelve con un unico numero de cobertura. Una ciudad inteligente obliga a distinguir entre alcance radio, carga de trafico e interferencia. El objetivo del reto es demostrar con base fisica y matematica que la solucion de red debe cambiar cuando cambia la casuistica operativa.

## 2. Estado del arte

La evolucion hacia LTE y 5G consolida OFDMA, programacion dinamica de recursos y adaptacion MCS. En paralelo, los modelos de propagacion urbanos y suburbanos siguen siendo la base del dimensionamiento inicial. Para el plano de capacidad, Erlang B sigue siendo una herramienta docente valida cuando se desea estimar bloqueo y area maxima por celda.

### 2.1 Contexto radio moderno

| modulation | design_tradeoff | typical_use | interpretation |
| --- | --- | --- | --- |
| QPSK | High robustness | Cell edge and difficult propagation | Lower spectral efficiency, lower SNR need |
| 16QAM | Balanced | Typical urban load | Intermediate throughput and robustness |
| 64QAM | High throughput | Good SINR zones | Higher spectral efficiency at higher SNR |
| 256QAM | Peak efficiency | Excellent channel quality | Representative of modern LTE/5G adaptation logic |

## 3. Metodologia

La metodologia reproduce exactamente la secuencia pedida en la guia docente: ruido, sensibilidad, perdida maxima, radio por cobertura, trafico por usuario, densidad de trafico, canales utiles, capacidad Erlang B y radio por capacidad. El criterio final adopta siempre el menor radio entre cobertura y capacidad.

### 3.1 Parametros base del sistema

| parameter | value | engineering_role |
| --- | --- | --- |
| Operating frequency | 1800 MHz | Shared by both scenarios |
| System bandwidth | 20 MHz | Used for thermal noise |
| Base station transmit power | 43 dBm | Equivalent to 20 W |
| TX antenna gain | 18 dBi | Base station sector antenna |
| RX antenna gain | 0 dBi | Mobile terminal |
| Additional losses | 12 dB | Cables, connectors and design margin |
| Receiver noise figure | 7 dB | NF for sensitivity estimate |
| Implementation losses | 2 dB | L_impl term in sensitivity |
| Blocking probability | 2.00% | GoS objective for Erlang B |
| Total physical channels | 100 | Simplified PRB-like capacity pool |

### 3.2 Objetivos por escenario

| scenario | environment | density | design_priority | required_analysis |
| --- | --- | --- | --- | --- |
| A_distrito_financiero | Dense urban core | 2500 active users/km2 | Coverage plus strong capacity pressure | Three sectors per site and N = 3, 4, 7 comparison |
| B_festival_global | Open suburban esplanade | 8000 active users/km2 | Extreme temporal congestion | Omnidirectional cells plus cell splitting evaluation |

## 4. Escenarios

### 4.1 Escenario A - Distrito financiero

El distrito financiero parte de 250.0 Erl/km2, una SNR requerida de 15 dB y una arquitectura de tres sectores por sitio con analisis de N = 3, 4 y 7.

### 4.2 Escenario B - Festival global

El festival parte de 666.7 Erl/km2, una SNR requerida de 5 dB, celdas omnidireccionales y evaluacion explicita de cell splitting.

## 5. Resultados

### 5.1 Cobertura

| scenario | thermal_noise_dbm | receiver_sensitivity_dbm | max_path_loss_db | coverage_radius_km | traffic_per_user_erlang | traffic_density_erlang_km2 | target_area_km2 | propagation_model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A_distrito_financiero | -93.9897 | -76.9897 | 125.99 | 0.552793 | 0.1 | 250 | 1 | L_p = 135 + 35 log10(d) |
| B_festival_global | -93.9897 | -86.9897 | 135.99 | 3.41185 | 0.0833333 | 666.667 | 1 | L_p = 120 + 30 log10(d) |

### 5.2 Capacidad en el distrito financiero

| reuse_factor_n | reuse_ratio_d_over_r | reuse_distance_km_if_design_radius | channels_per_site | channels_per_sector | sector_capacity_erlang | site_capacity_erlang | capacity_area_km2 | capacity_radius_km | coverage_radius_km | design_radius_km | design_area_km2 | sectorized_sir_db | omnidirectional_sir_db | sir_margin_db | limiting_factor | sites_for_target_area | recommended |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 0.492776 | 33 | 11 | 5.84153 | 17.5246 | 0.0700984 | 0.164259 | 0.552793 | 0.164259 | 0.0700984 | 13.6889 | 8.91773 | -1.31106 | capacity | 15 | False |
| 4 | 3.4641 | 0.448365 | 25 | 8 | 3.62705 | 10.8812 | 0.0435246 | 0.129432 | 0.552793 | 0.129432 | 0.0435246 | 15.8754 | 11.1042 | 0.875372 | capacity | 23 | True |
| 7 | 4.58258 | 0.32549 | 14 | 4 | 1.09226 | 3.27678 | 0.0131071 | 0.0710277 | 0.552793 | 0.0710277 | 0.0131071 | 20.1285 | 15.3573 | 5.12854 | capacity | 77 | False |

### 5.3 Capacidad y splitting en el festival

| channels_per_cell | cell_capacity_erlang | capacity_area_km2 | capacity_radius_km | coverage_radius_km | design_radius_km | design_area_km2 | limiting_factor | sites_for_target_area |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | 87.972 | 0.131958 | 0.225368 | 3.41185 | 0.225368 | 0.131958 | capacity | 8 |

| split_stage | radius_km | area_km2 | cells_per_original_footprint | capacity_density_erlang_km2 | supported_users_km2 | demand_users_km2 | meets_demand | sites_for_target_area | recommended |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 3.41185 | 30.2435 | 1 | 2.90879 | 34.9055 | 8000 | False | 1 | False |
| 1 | 1.70593 | 7.56087 | 4 | 11.6352 | 139.622 | 8000 | False | 1 | False |
| 2 | 0.852963 | 1.89022 | 16 | 46.5407 | 558.488 | 8000 | False | 1 | False |
| 3 | 0.426481 | 0.472555 | 64 | 186.163 | 2233.95 | 8000 | False | 3 | False |
| 4 | 0.213241 | 0.118139 | 256 | 744.65 | 8935.81 | 8000 | True | 9 | True |
| 5 | 0.10662 | 0.0295347 | 1024 | 2978.6 | 35743.2 | 8000 | True | 34 | False |
| 6 | 0.0533102 | 0.00738366 | 4096 | 11914.4 | 142973 | 8000 | True | 136 | False |

## 6. Discusion

En el distrito financiero, el radio por cobertura alcanza 0.553 km, pero el radio por capacidad recomendado cae a 0.129 km. Esto demuestra que la celda se dimensiona por carga y no por alcance.
En el festival, la diferencia es todavia mas extrema: la cobertura teorica es 3.412 km mientras que la capacidad util solo sostiene 0.225 km. El problema dominante es la densidad de usuarios.

## 7. Supuestos y trazabilidad

| assumption | applied_value | justification |
| --- | --- | --- |
| Reference target area | 1 km2 for both scenarios | The statement asks for the number of cells over a proposed target area but does not provide a fixed value. A common normalized 1 km2 area is assumed to compare cell density without bias. |
| Channel partition in scenario A | floor(100 / N) channels per site, then uniform split across 3 sectors | The statement requests N = 3, 4, 7 and three sectors per site, but it does not define a more detailed PRB scheduler. The uniform split is the simplest reproducible assumption. |
| Interference approximation | 2 first-tier interferers for sectorized cells and 6 for omnidirectional reference | This is the standard first-tier hexagonal approximation used to compare reuse strategies in teaching-oriented planning exercises. |
| Hexagonal geometry | Regular hexagonal cell area model | Needed to convert traffic-limited area into an equivalent cell radius and then into the number of required sites. |
| Modern radio context | OFDMA/LTE/5G design logic with adaptive MCS | The statement explicitly asks for a modern mobile-network framing even though the numerical exercise is simplified to link budget and Erlang B. |

## 8. Validacion frente a la rubrica

| rubric_area | project_evidence | why_it_matters |
| --- | --- | --- |
| Structure and presentation | Static web includes summary, scenarios, assumptions and code section | Supports rubric presentation block |
| State of the art | Project exports a modulation context table and OFDMA framing | Connects calculations with modern mobile systems |
| Methodology | Main pipeline reproduces noise, sensitivity, coverage, capacity, reuse and splitting | Step-by-step reproducibility is explicit |
| Mathematical precision | Outputs keep units, formulas and CSV traces | Facilitates annex verification |
| Discussion | Root web explains limiting factors and design trade-offs | Moves beyond raw numbers |
| Conclusions and future view | Report builder includes recommendations and 2030 extension note | Aligns with final rubric block |

## 9. Conclusiones

La solucion adoptada para el distrito financiero es N=4 con tres sectores por sitio. La solucion adoptada para el festival es cell splitting hasta S4. Ambas decisiones se justifican porque son las primeras que satisfacen simultaneamente los criterios de cobertura, capacidad e interferencia bajo las hipotesis declaradas.

### 9.1 Nueva Pangea 2030

Si la densidad de usuarios creciera, la evolucion natural del proyecto apuntaria a small cells, mas espectro, beamforming, slicing y edge computing. El codigo del proyecto deja la base cuantitativa para ensayar esas extensiones.