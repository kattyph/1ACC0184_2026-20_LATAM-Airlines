"""Funciones compartidas. Fuente: OpenFlights (2017) https://openflights.org/data"""
import pandas as pd

BASE = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/"
COLS_AIRPORTS = ["AirportID", "Name", "City", "Country", "IATA", "ICAO", "Latitude",
                 "Longitude", "Altitude", "Timezone", "DST", "TZ_database", "Type", "Source"]
COLS_ROUTES = ["airline", "airline_id", "source_airport", "source_airport_id",
               "dest_airport", "dest_airport_id", "codeshare", "stops", "equipment"]

def cargar():
    a = pd.read_csv(BASE + "airports.dat", header=None, names=COLS_AIRPORTS,
                    na_values=["\\N"], keep_default_na=False)
    r = pd.read_csv(BASE + "routes.dat", header=None, names=COLS_ROUTES,
                    na_values=["\\N"], keep_default_na=False)
    # Limpieza: IATA valido, tipo airport, solo aeropuertos con al menos 1 ruta
    a = a[(a["IATA"].str.len() == 3) & (a["Type"] == "airport")]
    con_ruta = set(r["source_airport"]) | set(r["dest_airport"])
    a = a[a["IATA"].isin(con_ruta)]
    return a, r

def extraer(prefijos_tz, salida):
    """Guarda en CSV los aeropuertos cuya zona horaria (TZ_database) empieza por los prefijos."""
    a, _ = cargar()
    parte = a[a["TZ_database"].fillna("").str.split("/").str[0].isin(prefijos_tz)]
    parte.to_csv(salida, index=False)
    print(f"{salida}: {len(parte)} aeropuertos (nodos)")
