SELECT
    event_type,
    COUNT(*) AS event_count,

    (COUNT(*) * 100.0 / sum(COUNT(*)) OVER ()) AS percentage
    FROM customers
    GROUP BY event_type
    ORDER BY event_count DESC;