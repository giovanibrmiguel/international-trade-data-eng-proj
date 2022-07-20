SELECT
    stg_country_product_trade.transaction_id,
    stg_country_product_trade.country_id,
    stg_country_product_trade.partner_country_id,
    stg_country_product_trade.country_code,
    stg_country_product_trade.partner_country_code,
    location.location_name_short_en AS country_name,
    partner_location.location_name_short_en AS partner_country_name,
    stg_country_product_trade.product_id,
    stg_country_product_trade.export_value,
    stg_country_product_trade.import_value,
    stg_country_product_trade.sitc_eci,
    stg_country_product_trade.sitc_coi,
    stg_country_product_trade.transaction_date
FROM
    {{ ref('stg_country_product_trade')}} AS stg_country_product_trade
LEFT JOIN
    {{ ref('location')}} AS location
        ON stg_country_product_trade.country_id = location.location_id
LEFT JOIN
    {{ ref('location')}} AS partner_location
        ON stg_country_product_trade.partner_country_id = location.location_id
LIMIT 100