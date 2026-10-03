"""Unimos las 3 partes y crea airports.db (nodos = aeropuertos, aristas = rutas)."""
import sqlite3, glob
import pandas as pd
from comun import cargar

partes = [pd.read_csv(f) for f in sorted(glob.glob("../dataset/parte_*.csv"))]
airports = pd.concat(partes, ignore_index=True)
assert airports["IATA"].is_unique, "Hay aeropuertos repetidos entre partes"

_, routes = cargar()
iatas = set(airports["IATA"])
routes = routes[routes["source_airport"].isin(iatas) & routes["dest_airport"].isin(iatas)].drop_duplicates()

con = sqlite3.connect("../dataset/airports.db")
airports.to_sql("airports", con, if_exists="replace", index=False)
routes.to_sql("routes", con, if_exists="replace", index=False)
con.execute("CREATE INDEX idx_src ON routes(source_airport)")
con.execute("CREATE INDEX idx_dst ON routes(dest_airport)")
con.commit()
print("Nodos:", len(airports), "| Aristas:", len(routes))
