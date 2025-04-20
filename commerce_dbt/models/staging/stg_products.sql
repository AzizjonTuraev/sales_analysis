with source as (
    select * from {{ source('commerce', 'products') }}
),

renamed as (
    select
        product_id,
        product_name,
        product_categories_id,
        price,
        current_timestamp as loaded_at
    from source
)

select * from renamed