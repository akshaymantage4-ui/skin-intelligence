from pathlib import Path
import json
import pandas as pd

DATASET = Path(__file__).resolve().parent.parent / "data" / "ingredient_reference.csv"

INTERACTIONS = {
    frozenset(("retinol", "salicylic acid")): "Using both in the same routine may increase irritation; introduce cautiously and consider separating routines.",
    frozenset(("retinol", "glycolic acid")): "Using both in the same routine may increase irritation; consider alternating nights.",
    frozenset(("retinol", "lactic acid")): "Using both in the same routine may increase irritation; consider alternating nights.",
    frozenset(("retinol", "mandelic acid")): "Using both in the same routine may increase irritation; consider alternating nights.",
    frozenset(("salicylic acid", "glycolic acid")): "Combining exfoliating acids can increase irritation; avoid stacking if sensitive.",
}

def load_reference():
    if not DATASET.exists():
        raise FileNotFoundError(f"Missing ingredient reference: {DATASET}")
    df = pd.read_csv(DATASET).fillna("")
    df.columns = [c.strip() for c in df.columns]
    return df

def analyze(names: list[str]):
    df = load_reference()
    results, not_found = [], []
    for raw in names:
        name = raw.strip()
        if not name:
            continue
        key = name.casefold()
        matches = df[(df.inci_name.astype(str).str.casefold() == key) | (df.display_name.astype(str).str.casefold() == key)]
        if matches.empty:
            not_found.append(name)
            continue
        row = matches.iloc[0]
        results.append({
            "inci_name": row.inci_name,
            "display_name": row.display_name,
            "function": row.function,
            "reference_flags": {
                "fungal_acne_trigger": int(row.fa_trigger),
                "comedogenic": int(row.comedogenic),
                "fragrance": int(row.fragrance),
                "eu_allergen": int(row.eu_allergen),
                "pregnancy_caution": int(row.pregnancy_caution),
            },
        })
    found_keys = [str(x["display_name"]).casefold() for x in results]
    interactions = []
    for pair, message in INTERACTIONS.items():
        if pair.issubset(set(found_keys)):
            interactions.append({"ingredients": sorted(pair), "message": message})
    return {
        "submitted_count": len(names),
        "matched_count": len(results),
        "not_found": not_found,
        "ingredients": results,
        "interactions": interactions,
        "notice": "Reference attributes and interaction guidance only; not a medical diagnosis or individualized safety determination.",
    }
