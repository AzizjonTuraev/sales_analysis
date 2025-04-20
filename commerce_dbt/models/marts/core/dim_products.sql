with products as (
    select * from {{ ref('stg_products') }}
),

categories as (
    select * from {{ ref('stg_product_categories') }}
),

final as (
    select
        p.product_id,
        p.product_name,
        p.price,
        c.product_categories,
        case
            when p.price < 20 then 'Budget'
            when p.price between 20 and 50 then 'Standard'
            else 'Premium'
        end as price_segment
    from products p
    left join categories c on p.product_categories_id = c.product_categories_id
)

select * from final