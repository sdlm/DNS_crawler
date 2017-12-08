select i.id, i.name, count(p.id) as price_changes
from DnsItemModel i, Price p
WHERE p.item = i.id
GROUP BY i.id
ORDER BY price_changes DESC;