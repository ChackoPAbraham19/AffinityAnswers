SELECT f.rfam_acc, f.rfam_id, MAX(s.length) AS max_length
FROM family f
JOIN full_region fr ON f.rfam_acc = fr.rfam_acc
JOIN rfamseq s ON fr.rfamseq_acc = s.rfamseq_acc
GROUP BY f.rfam_acc, f.rfam_id
HAVING MAX(s.length) > 1000000
ORDER BY max_length DESC, f.rfam_acc
LIMIT 15 OFFSET 120;