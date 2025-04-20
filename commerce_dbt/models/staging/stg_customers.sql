with source as (
    select * from {{ source('commerce', 'customers') }}
),

renamed as (
    select
        customer_id,
        name,
        location,
        gender,
        -- Add any necessary casting or transformations
        current_timestamp as loaded_at
    from source
)

select * from renamed