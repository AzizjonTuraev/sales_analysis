-- snapshots/snap_products.sql
{% snapshot snap_products %}

{{
  config(
    target_schema='snapshots',
    unique_key='product_id',
    strategy='check',
    check_cols=['price']
  )
}}

SELECT * FROM {{ source('commerce', 'products') }}

{% endsnapshot %}