with source as (
    select * from {{ source('commerce', 'product_categories') }}
),

renamed as (
    select
        product_categories_id,
        product_categories,
        current_timestamp as loaded_at
    from source
)

select * from renamed