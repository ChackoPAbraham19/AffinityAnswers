SELECT COUNT(DISTINCT species) AS named_acacia_species FROM taxonomy
WHERE species LIKE 'Acacia %'
  AND species NOT LIKE 'Acacia sp.%'
  AND species NOT LIKE 'Acacia % x %'
  AND species NOT LIKE 'Acacia environmental sample%'
  AND tax_string LIKE '%Fabaceae%';