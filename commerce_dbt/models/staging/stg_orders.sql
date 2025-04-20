with source as (
    select * from {{ source('commerce', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        store_id,
        -- Add date transformations if needed
        order_date::date,
        current_timestamp as loaded_at
    from source
)

select * from renamed