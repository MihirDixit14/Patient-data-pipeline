-- Q1: Observation types with the most out-of-range values
SELECT observation_type,COUNT(*) AS total_observations,
        SUM(CASE WHEN value<ref_range_low OR value>ref_range_high THEN 1 ELSE 0 END) AS out_of_range_count,
        ROUND(100.0*SUM(CASE WHEN value<ref_range_low OR value>ref_range_high THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_out_of_range
FROM observations
WHERE ref_range_low IS NOT NULL
        AND ref_range_high IS NOT NULL
        AND value IS NOT NULL

GROUP BY observation_type
ORDER BY out_of_range_count DESC;