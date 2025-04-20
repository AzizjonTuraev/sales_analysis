with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('dim_products') }}
)

select
    o.order_id,
    o.customer_id,
    o.store_id,
    o.order_date,
    oi.order_item_id,
    oi.product_id,
    p.product_name,
    p.product_categories,
    p.price_segment,
    oi.quantity,
    p.price as unit_price,
    (p.price * oi.quantity) as total_price,
    current_timestamp as loaded_at
from orders o
join order_items oi on o.order_id = oi.order_id
join products p on oi.product_id = p.product_id