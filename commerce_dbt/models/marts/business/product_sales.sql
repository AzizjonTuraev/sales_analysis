with orders as (
    select * from {{ ref('fct_orders') }}
),

products as (
    select * from {{ ref('dim_products') }}
)

select
    p.product_id,
    p.product_name,
    p.product_categories,
    p.price_segment,
    sum(o.quantity) as total_units_sold,
    sum(o.total_price) as total_revenue,
    avg(o.unit_price) as avg_selling_price,
    count(distinct o.order_id) as order_count
from products p
left join orders o on p.product_id = o.product_id
group by 1, 2, 3, 4
order by total_revenue desc