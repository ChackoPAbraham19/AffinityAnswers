SELECT t.species as "Species of wheat with max length", r.rfamseq_acc, r.length
FROM rfamseq r
JOIN taxonomy t ON r.ncbi_id = t.ncbi_id
WHERE t.species LIKE 'Triticum %'
ORDER BY r.length DESC
LIMIT 1;