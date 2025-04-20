{#
/* 
Purpose: Transforms raw order_items data into standardized structure
Owner: Data Team
Freshness: Source data updates daily at 2AM UTC
*/
#}


with source as (
    select * from {{ source('commerce', 'order_items') }}
),

renamed as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        current_timestamp as loaded_at
    from source
)

select * from renamed