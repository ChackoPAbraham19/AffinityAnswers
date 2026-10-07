# Q2 – Rfam SQL queries

SQL queries against the public [Rfam](https://docs.rfam.org/en/latest/database.html) MySQL database.

| File | Question it answers |
|------|---------------------|
| `sub_q1.sql` | How many named species of *Acacia* (family Fabaceae) are there? Excludes unnamed (`sp.`), hybrid (`x`) and environmental-sample entries. |
| `sub_q2.sql` | Which species of wheat (*Triticum*) has the longest DNA sequence? |
| `sub_q3.sql` | Families whose longest sequence exceeds 1,000,000 bases, ordered by length: page 9 of results (15 per page, offset 120). |

## Running

Needs only a MySQL client. The database is public and read-only, with no password:

```bash
mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro Rfam < sub_q1.sql
```

Swap in `sub_q2.sql` or `sub_q3.sql` to run the others.
