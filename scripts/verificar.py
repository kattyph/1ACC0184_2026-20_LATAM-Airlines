"""Verificamos el minimo de 500 nodos por integrante y que las partes sean disjuntas."""
import pandas as pd
partes = {"A (America)": "../dataset/parte_A_america.csv",
          "B (Asia+Oceania)": "../dataset/parte_B_asia_oceania.csv",
          "C (Europa+Africa)": "../dataset/parte_C_europa_africa.csv"}
vistos, total = set(), 0
print(f"{'Integrante':<20}{'Nodos':>8}  Minimo 500")
for k, f in partes.items():
    ids = set(pd.read_csv(f)["IATA"])
    assert not (ids & vistos), f"Nodos repetidos en {k}"
    vistos |= ids; total += len(ids)
    print(f"{k:<20}{len(ids):>8}  {'OK' if len(ids) >= 500 else 'NO CUMPLE'}")
print(f"{'TOTAL':<20}{total:>8}  {'OK' if total >= 1500 else 'NO CUMPLE'}")
