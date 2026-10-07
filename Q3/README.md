# Q3 – Company list from a CSV URL

`company.sh` asks for the URL of a CSV file of companies, checks that the URL is valid and reachable, downloads it, and prints each company's name, location and founding year, sorted by year (oldest first).

## Requirements

`bash`, `curl` and `gawk` (GNU awk). On Debian/Ubuntu, `gawk` may need installing: `sudo apt install gawk`.

## Running

```bash
chmod +x company.sh
./company.sh
# Enter the URL :
# https://example.com/companies.csv
```

## How it works

1. **Cleans the input:** strips whitespace and any `?query` part from the URL.
2. **Validates it:** checks the URL format with a regex, then makes a `HEAD` request and requires an HTTP 200 response.
3. **Downloads the CSV:** saves it to a temporary `data.csv`, which is removed on exit by a `trap`.
4. **Parses it:** uses `gawk` with `FPAT`, so quoted fields that contain commas (e.g. `"Mumbai, India"`) stay intact. It reads company name from column 2, location from column 5 and founded from column 8.
5. **Normalises the year:** values like `1851 (1892)` keep the first 4-digit year. Missing years show as `N/A` and sort last.
6. **Prints the table:** sorted by year, then by name, as aligned columns.
