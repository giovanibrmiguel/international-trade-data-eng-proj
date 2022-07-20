SELECT
    FARM_FINGERPRINT(CONCAT(location_code, partner_code, CAST(product_id AS STRING), CAST(year AS STRING), CAST(import_value AS STRING), CAST(export_value AS STRING))) AS transaction_id,
    location_id AS country_id,
    partner_id AS partner_country_id,
    location_code AS country_code,
    partner_code AS partner_country_code,
    product_id,
    export_value,
    import_value,
    sitc_eci,
    sitc_coi,
    year AS transaction_date
FROM
    {{ source('data_lake','country_product_trade') }}