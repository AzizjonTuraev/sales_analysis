with stores as (
    select * from {{ ref('stg_stores') }}
),

final as (
    select
        store_id,
        location
        -- , Add any geographic transformations here
        -- split_part(location, ',', 1) as city,
        -- split_part(location, ',', 2) as state
    from stores
)

select * from final