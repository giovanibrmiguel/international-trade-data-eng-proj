SELECT
    stg_country_product_trade.transaction_id,
    stg_country_product_trade.product_id,
    stg_country_product_trade.country_id,
    stg_country_product_trade.partner_country_id,
    stg_country_product_trade.country_code,
    stg_country_product_trade.partner_country_code,
    location.location_name_short_en AS country_name,
    partner_location.location_name_short_en AS partner_country_name,
    product_section.sitc_product_name_short_en AS product_section,
    product_type.sitc_product_name_short_en AS product_type,
    product_detail.sitc_product_name_short_en AS product_detail,
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
        ON stg_country_product_trade.partner_country_id = partner_location.location_id
LEFT JOIN
    {{ ref('sitc_product') }} AS product_detail
        ON stg_country_product_trade.product_id = product_detail.product_id
LEFT JOIN
    {{ ref('sitc_product') }} AS product_type
        ON product_detail.parent_id = product_type.product_id
LEFT JOIN
    {{ ref('sitc_product') }} AS product_section
        ON product_type.parent_id = product_section.product_id