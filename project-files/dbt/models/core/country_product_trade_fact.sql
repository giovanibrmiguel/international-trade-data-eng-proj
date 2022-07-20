SELECT
    transaction_id,
    location_id,
    partner_id,
    location_code,
    partner_code,
    product_id,
    export_value,
    import_value,
    sitc_eci,
    sitc_coi,
    transaction_date
FROM
    {{ ref('stg_country_product_trade')}}