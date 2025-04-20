with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('dim_products') }}
), 

product_categories as (
    select * from {{ ref('stg_product_categories') }}
)


select
    o.order_date,
    p.product_name,
    p.product_categories,
    oi.quantity,
    p.price as unit_price,
    (p.price * oi.quantity) as total_price,
    EXTRACT(DOW FROM o.order_date) AS day_of_week,
    EXTRACT(WEEK FROM o.order_date) AS week,
    EXTRACT(MONTH FROM o.order_date) AS month,
    EXTRACT(YEAR FROM o.order_date) AS year
from orders o
join order_items oi on o.order_id = oi.order_id
join products p on oi.product_id = p.product_id
-- JOIN product_categories pc ON p.product_categories_id = pc.product_categories_id


