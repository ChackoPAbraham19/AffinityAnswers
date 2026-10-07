# AffinityAnswers

Solutions to the Affinity Answers assessment. Each question lives in its own folder with its own README.

| Folder | Task | Language |
|--------|------|----------|
| [`Q1/`](Q1/) | Web scraper: search mdcomputers.in for a term and output the listed products as JSON | Python (Playwright) |
| [`Q2/`](Q2/) | SQL queries against the public Rfam database | SQL (MySQL) |
| [`Q3/`](Q3/) | Shell script: download a CSV of companies from a URL and list them sorted by founding year | Bash + gawk |

## Quick start

```bash
# Q1
cd Q1
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/playwright install chromium
.venv/bin/python scraper.py "external harddrive"
cd ..

# Q2
mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro Rfam < Q2/sub_q1.sql

# Q3
bash Q3/company.sh
```

See each folder's README for details and design notes.
