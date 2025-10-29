#Junjin Tan 
#6687-1681
#junjin@umich.edu
#SI 201 Project #1
#Worked alone, used ChatGPT to help reformat code and also assist with making sure my files were in the right repository 
#Used the penguins dataset 
#Columns used: island, year, sex
#Calculations performed: percentage of male penguins from Biscoe, and average year in dataset

import csv

with open("penguins.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

def analyze_penguins(csv_path: str, out_path: str = "penguin_results.txt") -> None:
    """Read penguins.csv, compute stats, and write a text report."""
    total_valid_island_sex = 0      # rows with BOTH island + sex present
    biscoe_male_count = 0

    year_sum = 0
    year_count = 0

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # --- % Male from Biscoe ---
            island = (row.get("island") or "").strip()
            sex = (row.get("sex") or "").strip().lower()

            if island and sex:  # only count rows where both columns are present
                total_valid_island_sex += 1
                if island == "Biscoe" and sex.startswith("male"):
                    biscoe_male_count += 1

            # --- Average Year ---
            y = (row.get("year") or "").strip()
            if y.isdigit():
                year_sum += int(y)
                year_count += 1

    # Safeguards against division by zero
    biscoe_male_pct = (
        (biscoe_male_count / total_valid_island_sex) * 100
        if total_valid_island_sex > 0 else 0.0
    )
    avg_year = (year_sum / year_count) if year_count > 0 else 0.0

    # Console output (optional)
    print(f"% of male penguins from Biscoe: {biscoe_male_pct:.2f}% "
          f"(based on {total_valid_island_sex} rows with island+sex)")
    print(f"Average year: {avg_year:.2f} (from {year_count} rows with a year)")

    # Write results to a .txt file
    with open(out_path, "w") as out:
        out.write("Penguin Dataset Analysis Results\n")
        out.write("---------------------------------\n")
        out.write(f"Rows with island+sex present: {total_valid_island_sex}\n")
        out.write(f"Male penguins from Biscoe: {biscoe_male_count}\n")
        out.write(f"Percentage male from Biscoe: {biscoe_male_pct:.2f}%\n")
        out.write(f"\nRows with a valid year: {year_count}\n")
        out.write(f"Average year: {avg_year:.2f}\n")

if __name__ == "__main__":
    analyze_penguins("penguins.csv")

# --- functions under test  ---

def calculate_male_biscoe_pct(rows):
    """
    Inputs: rows = list[dict] with at least 'island' and 'sex'
    Returns: dict with keys:
      - total_island_sex_rows
      - biscoe_males
      - biscoe_male_pct  (0.0 if denominator is 0)
    """
    total_valid = 0
    biscoe_male_count = 0

    for r in rows:
        island = (r.get("island") or "").strip()
        sex = (r.get("sex") or "").strip().lower()

        if island and sex:                
            total_valid += 1
            if island == "Biscoe" and sex.startswith("male"):
                biscoe_male_count += 1

    pct = (biscoe_male_count / total_valid * 100) if total_valid else 0.0
    return {
        "total_island_sex_rows": total_valid,
        "biscoe_males": biscoe_male_count,
        "biscoe_male_pct": pct,
    }


def calculate_average_year(rows):
    """
    Inputs: rows = list[dict] with key 'year' (string)
    Returns: dict with keys:
      - year_sum
      - year_count
      - avg_year  (0.0 if count is 0)
    """
    s = 0
    n = 0
    for r in rows:
        y = (r.get("year") or "").strip()
        if y.isdigit():
            s += int(y)
            n += 1
    avg = s / n if n else 0.0
    return {"year_sum": s, "year_count": n, "avg_year": avg}


# --- unit tests ---

import unittest

class TestPenguinCalcs(unittest.TestCase):

    # ===== calculate_male_biscoe_pct =====
    def test_male_biscoe_typical_mix(self):
        rows = [
            {"island": "Biscoe", "sex": "male"},
            {"island": "Biscoe", "sex": "female"},
            {"island": "Dream",  "sex": "male"},
        ]
        stats = calculate_male_biscoe_pct(rows)
        self.assertEqual(stats["total_island_sex_rows"], 3)
        self.assertEqual(stats["biscoe_males"], 1)
        self.assertAlmostEqual(stats["biscoe_male_pct"], 33.3333, places=3)

    def test_male_biscoe_case_whitespace(self):
        rows = [
            {"island": "Biscoe", "sex": " Male  "},  
            {"island": "Biscoe", "sex": "FEMALE"},
        ]
        stats = calculate_male_biscoe_pct(rows)
        self.assertEqual(stats["biscoe_males"], 1)
        self.assertEqual(stats["total_island_sex_rows"], 2)
        self.assertAlmostEqual(stats["biscoe_male_pct"], 50.0, places=2)

    def test_male_biscoe_missing_fields_ignored(self):
        rows = [
            {"island": "Biscoe", "sex": ""},              
            {"island": "",       "sex": "male"},           
            {"island": "Dream",  "sex": "male"},           
            {"island": "Biscoe", "sex": "male"},           
        ]
        stats = calculate_male_biscoe_pct(rows)
        self.assertEqual(stats["total_island_sex_rows"], 2)
        self.assertEqual(stats["biscoe_males"], 1)
        self.assertAlmostEqual(stats["biscoe_male_pct"], 50.0, places=2)

    def test_male_biscoe_empty_input(self):
        stats = calculate_male_biscoe_pct([])
        self.assertEqual(stats["total_island_sex_rows"], 0)
        self.assertEqual(stats["biscoe_males"], 0)
        self.assertEqual(stats["biscoe_male_pct"], 0.0)

    # ===== calculate_average_year =====
    def test_avg_year_typical(self):
        rows = [{"year": "2007"}, {"year": "2008"}, {"year": "2009"}]
        stats = calculate_average_year(rows)
        self.assertEqual(stats["year_sum"], 6024)
        self.assertEqual(stats["year_count"], 3)
        self.assertAlmostEqual(stats["avg_year"], 2008.0, places=2)

    def test_avg_year_ignores_invalid(self):
        rows = [{"year": "2007"}, {"year": ""}, {"year": "abc"}, {"year": " 2008 "}]
        stats = calculate_average_year(rows)
        self.assertEqual(stats["year_count"], 2)
        self.assertEqual(stats["year_sum"], 4015)
        self.assertAlmostEqual(stats["avg_year"], 2007.5, places=2)

    def test_avg_year_all_invalid(self):
        rows = [{"year": ""}, {"year": "n/a"}, {"year": "20O8"}]  
        stats = calculate_average_year(rows)
        self.assertEqual(stats["year_count"], 0)
        self.assertEqual(stats["year_sum"], 0)
        self.assertEqual(stats["avg_year"], 0.0)

    def test_avg_year_spaces_only(self):
        rows = [{"year": "   "}, {"year": "2008"}]
        stats = calculate_average_year(rows)
        self.assertEqual(stats["year_count"], 1)
        self.assertEqual(stats["year_sum"], 2008)
        self.assertAlmostEqual(stats["avg_year"], 2008.0, places=2)

if __name__ == "__main__":
    unittest.main()

