# Auto-Ahorro por Default en Billeteras Digitales

Este repositorio contiene el código y la implementación de un experimento económico desarrollado en **oTree** para el **Laboratorio de Economía Experimental (LEEL)**.

El objetivo del experimento es analizar cómo los mecanismos de **ahorro automático (defaults de ahorro)** influyen en las decisiones de consumo y ahorro de los individuos cuando reciben ingresos periódicos y enfrentan posibles shocks financieros.

El proyecto busca evaluar si una política de _“save first”_ —en la cual una parte del ingreso se destina automáticamente al ahorro— puede modificar el comportamiento financiero de los participantes en comparación con un escenario donde el ahorro depende únicamente de decisiones activas.

---

## Objetivo del experimento

El experimento estudia el impacto de un **mecanismo de auto-ahorro predeterminado** sobre el comportamiento económico individual. En particular, se busca analizar:

- Si los participantes **ahorran más cuando existe un default automático**.
- Cómo los individuos ajustan sus decisiones de **consumo y ahorro manual**.
- Qué ocurre cuando enfrentan **shocks inesperados de liquidez**.
- Si la existencia de un mecanismo automático mejora la **capacidad de acumulación de ahorro**.

Este tipo de intervención se inspira en políticas de economía del comportamiento aplicadas en productos financieros digitales, como funciones de ahorro automático dentro de billeteras electrónicas o aplicaciones bancarias.

---

## Diseño experimental

El experimento consiste en una serie de decisiones económicas repetidas en múltiples rondas.

Características principales del diseño:

- **Número de rondas:** 12
- **Ingreso por ronda:** valor aleatorio entre 80 y 120 unidades experimentales, igual para todos.
- **Tratamientos:**
  - **Control:** los participantes deciden cuánto ahorrar manualmente
  - **Tratamiento:** el sistema aplica automáticamente un ahorro del **10% del ingreso**

- **Decisiones del participante:**
  - Ahorro manual
  - Consumo

- **Shock financiero:** en la **ronda 8** ocurre una reducción inesperada del balance líquido
- **Resultados observados:**
  - Ahorro acumulado
  - Consumo
  - Balance líquido

El experimento se implementa utilizando **oTree**, una plataforma ampliamente utilizada para experimentos en economía y ciencias sociales.

---

## Autores

Proyecto desarrollado para el **Laboratorio de Economía Experimental – Taller 2026**.

- Isabella Agurto — UDEP
- Heidi Alpiste — UPC
- Diego Fernandez — UDEP
- Manuel Taco — UP

---
