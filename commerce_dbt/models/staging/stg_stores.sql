with source as (
    select * from {{ source('commerce', 'stores') }}
),

renamed as (
    select
        store_id,
        location
--        ,current_timestamp as loaded_at
    from source
)

select * from renamed