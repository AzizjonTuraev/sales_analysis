with customers as (
    select * from {{ ref('stg_customers') }}
),

customer_orders as (
    select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders
    from {{ ref('stg_orders') }}
    group by 1
),

final as (
    select
        c.customer_id,
        c.name,
        c.location,
        c.gender,
        co.first_order_date,
        co.most_recent_order_date,
        coalesce(co.number_of_orders, 0) as number_of_orders,
        case
            when co.number_of_orders is null then 'New'
            when co.number_of_orders = 1 then 'One-time'
            when co.number_of_orders between 2 and 5 then 'Regular'
            else 'Loyal'
        end as customer_segment
    from customers c
    left join customer_orders co on c.customer_id = co.customer_id
)

select * from final