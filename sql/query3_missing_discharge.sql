-- Q3: Percentage of encounters missing a discharge date grouped by status
SELECT
    status,
    COUNT(*)                                                        AS total_encounters,
    SUM(CASE WHEN discharge_date IS NULL THEN 1 ELSE 0 END)        AS missing_discharge,
    ROUND(
        100.0 * SUM(CASE WHEN discharge_date IS NULL THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                               AS pct_missing
FROM encounters
GROUP BY status
ORDER BY pct_missing DESC;
