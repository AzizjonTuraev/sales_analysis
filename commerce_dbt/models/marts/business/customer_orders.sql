with orders as (
    select * from {{ ref('fct_orders') }}
),

customers as (
    select * from {{ ref('dim_customers') }}
)

select
    c.customer_id,
    c.name,
    c.location,
    c.customer_segment,
    count(distinct o.order_id) as order_count,
    sum(o.total_price) as total_spend,
    avg(o.total_price) as avg_order_value,
    max(o.order_date) as last_order_date,
    current_date - max(o.order_date) as days_since_last_order
from customers c
left join orders o on c.customer_id = o.customer_id
group by 1, 2, 3, 4
order by total_spend desc


