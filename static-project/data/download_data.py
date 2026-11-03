"""
Download data for the AI adoption project.

Usage (from your data-viz folder):
    pip install pandas requests openpyxl
    python download_data.py

Creates data/raw/ with:
    worldbank_wdi.csv, worldbank_countries.csv
    ilostat_emp_occ_1digit.csv, ilostat_emp_occ_2digit.csv
    oecd_ict_business_ai.csv (and oecd_ict_business_all.csv)

Two sources are manual downloads (see README notes printed at the end):
    Stanford AI Index public data (Google Drive)
    ILO GenAI exposure scores (Excel file on GitHub / PDF annex)
"""

import io
import os

import pandas as pd
import requests

OUT = os.path.join("data", "raw")
os.makedirs(OUT, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (student data-viz project)"}


def get(url, **kwargs):
    r = requests.get(url, headers=HEADERS, timeout=300, **kwargs)
    r.raise_for_status()
    return r


# ---------------------------------------------------------------------------
# 1. World Bank WDI (JSON API, no key needed)
# ---------------------------------------------------------------------------
WB_INDICATORS = {
    "NY.GDP.PCAP.PP.CD": "gdp_per_capita_ppp",
    "IT.NET.USER.ZS": "internet_users_pct",
    "SE.TER.ENRR": "tertiary_enrollment_pct",
    "SP.POP.TOTL": "population",
}


def download_worldbank():
    print("World Bank: downloading indicators...")
    rows = []
    for code, name in WB_INDICATORS.items():
        url = (
            f"https://api.worldbank.org/v2/country/all/indicator/{code}"
            "?format=json&date=2010:2024&per_page=20000"
        )
        meta, data = get(url).json()
        for d in data or []:
            rows.append(
                {
                    "iso3": d["countryiso3code"],
                    "country": d["country"]["value"],
                    "indicator_code": code,
                    "indicator": name,
                    "year": int(d["date"]),
                    "value": d["value"],
                }
            )
        print(f"  {code}: {len(data or [])} rows")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "worldbank_wdi.csv"), index=False)

    # Country metadata: region + income group (your hierarchy).
    meta, countries = get(
        "https://api.worldbank.org/v2/country?format=json&per_page=400"
    ).json()
    cdf = pd.DataFrame(
        {
            "iso3": c["id"],
            "country": c["name"],
            "region": c["region"]["value"],
            "income_group": c["incomeLevel"]["value"],
        }
        for c in countries
    )
    # Drop aggregates like "World" and "High income" (their region is "Aggregates").
    cdf = cdf[cdf["region"] != "Aggregates"]
    cdf.to_csv(os.path.join(OUT, "worldbank_countries.csv"), index=False)
    print(f"  country metadata: {len(cdf)} countries")


# ---------------------------------------------------------------------------
# 2. ILOSTAT employment by sex and occupation (ILO's bulk API)
#    _OCU_ = ISCO 1-digit major groups, _OC2_ = ISCO 2-digit sub-major groups
# ---------------------------------------------------------------------------
ILO_INDICATORS = {
    "EMP_TEMP_SEX_OCU_NB_A": "ilostat_emp_occ_1digit.csv",
    "EMP_TEMP_SEX_OC2_NB_A": "ilostat_emp_occ_2digit.csv",
}


def download_ilostat():
    print("ILOSTAT: downloading employment by occupation...")
    for ind, fname in ILO_INDICATORS.items():
        url = f"https://rplumber.ilo.org/data/indicator/?id={ind}&format=.csv"
        try:
            df = pd.read_csv(io.BytesIO(get(url).content), low_memory=False)
        except Exception as e:  # noqa: BLE001
            print(f"  {ind} FAILED ({e}). Download it manually instead:")
            print("  https://ilostat.ilo.org/data/ -> search 'Employment by sex and occupation'")
            continue
        # Keep 2010 onward to stay in a manageable size range.
        if "time" in df.columns:
            df = df[pd.to_numeric(df["time"], errors="coerce") >= 2010]
        df.to_csv(os.path.join(OUT, fname), index=False)
        print(f"  {ind}: {len(df):,} rows x {df.shape[1]} cols, "
              f"{df['ref_area'].nunique() if 'ref_area' in df else '?'} countries")


# ---------------------------------------------------------------------------
# 3. OECD ICT Access and Usage by Businesses (OECD Data Explorer SDMX API)
# ---------------------------------------------------------------------------
OECD_URL = (
    "https://sdmx.oecd.org/public/rest/data/"
    "OECD.STI.DEP,DSD_ICT_B@DF_BUSINESSES,/all"
    "?dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
)


def download_oecd():
    print("OECD: downloading ICT business usage (can take a minute)...")
    try:
        df = pd.read_csv(io.BytesIO(get(OECD_URL).content), low_memory=False)
    except Exception as e:  # noqa: BLE001
        print(f"  FAILED ({e}). The OECD API rate-limits; wait a few minutes and retry,")
        print("  or use https://data-explorer.oecd.org -> search 'ICT Access and Usage by Businesses'")
        print("  -> Download -> 'Filtered data in tabular text (CSV)'.")
        return
    df.to_csv(os.path.join(OUT, "oecd_ict_business_all.csv"), index=False)
    # Keep rows whose labels mention AI.
    text_cols = [c for c in df.columns if df[c].dtype == object]
    mask = pd.Series(False, index=df.index)
    for c in text_cols:
        mask |= df[c].astype(str).str.contains("artificial intelligence", case=False, na=False)
    ai = df[mask]
    ai.to_csv(os.path.join(OUT, "oecd_ict_business_ai.csv"), index=False)
    print(f"  all: {len(df):,} rows; AI-related: {len(ai):,} rows x {ai.shape[1]} cols")


if __name__ == "__main__":
    for step in (download_worldbank, download_ilostat, download_oecd):
        try:
            step()
        except Exception as e:  # noqa: BLE001
            print(f"  {step.__name__} failed: {e}")
    print(
        "\nManual downloads still needed (save into data/raw/):\n"
        "  * Stanford AI Index 2026 public data:\n"
        "    https://drive.google.com/drive/folders/1zJTOg0iR0j5SijCwFutwWvDt143lW277\n"
        "  * ILO GenAI exposure scores:\n"
        "    https://github.com/pgmyrek/POLAND_2025_GenAI_scores_6digit_occupations\n"
        "    (ISCO 4-digit table is also Annex 'Exposure by 4-digit ISCO-08 occupation' in\n"
        "     https://www.ilo.org/sites/default/files/2025-05/WP140_web.pdf)"
    )
