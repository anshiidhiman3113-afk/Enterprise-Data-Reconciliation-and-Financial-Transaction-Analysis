/*
-------------------------------------------------------
Retrieve Latest Customer Record
Enterprise Data Reconciliation Project
-------------------------------------------------------
*/

WITH latest_customer AS (

SELECT
    *,
    ROW_NUMBER() OVER(
        PARTITION BY user_id
        ORDER BY updated_at DESC
    ) AS rn

FROM customers

)

SELECT *

FROM latest_customer

WHERE rn = 1;
