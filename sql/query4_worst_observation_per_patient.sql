-- Q4: Each patient's single most abnormal observation
SELECT patient_id,observation_id,observation_type,value,ref_range_low,ref_range_high,
ROUND(MAX(CASE WHEN value<ref_range_low THEN ref_range_low-value 
        WHEN value>ref_range_high THEN value-ref_range_high
        ELSE 0 END
        ),2) AS deviation

FROM observations
WHERE value is NOT NULL 
    AND ref_range_low IS NOT NULL
    AND ref_range_high IS NOT NULL

GROUP BY patient_id
ORDER BY deviation DESC;
