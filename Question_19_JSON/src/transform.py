import pandas as pd

def transform_product_dimension(df:pd.DataFrame) -> pd.DataFrame:
    return df
def transform_store_dimension(df:pd.DataFrame) -> pd.DataFrame:
    return df
def transform_time_dimension(df:pd.DataFrame) -> pd.DataFrame:
    return df
def transform_suplier_dimension(sales_dm_df:pd.DataFrame) -> pd.DataFrame:
    supplier_cols=[
        "supplier_id",
        "supplier_name",
        "contact_email",
        "supplier_country",
        "reliability_score",
        "region_id",
        "promotion_id"
    ]
    return sales_dm_df[supplier_cols].drop_duplicates()

def transform_region_dimension(sales_dm_df:pd.DataFrame) -> pd.DataFrame:
    region_cols=[
        "region_id",
        "region_name",
        "region_country",
        "regional_manager"
    ]
    return sales_dm_df[region_cols].drop_duplicates()


def transform_promotion_dimension(sales_dm_df:pd.DataFrame) -> pd.DataFrame:
    promotion_cols=[
        "promotion_id",
        "promotion_name",
        "discount_percentage",
        "start_date",
        "end_date"
    ]
    return sales_dm_df[promotion_cols].drop_duplicates()

def transform_sales_fact(fact_df:pd.DataFrame,product_df:pd.DataFrame) -> pd.DataFrame:
    product_lookup=product_df[['product_id','supplier_id']]
    fact_df=fact_df.merge(product_lookup,on='product_id',how='left')
    return fact_df

def transform_all(dfs:dict) -> dict:
    return {
        "product_dimension":transform_product_dimension(dfs['product_dimension']),
        "store_dimension":transform_store_dimension(dfs['store_dimension']),
        "time_dimension":transform_time_dimension(dfs['time_dimension']),
        "supplier_dimension":transform_suplier_dimension(dfs['sales_dimension']),
        "region_dimension":transform_region_dimension(dfs["sales_dimension"]),
        "promotion_dimension":transform_promotion_dimension(dfs['sales_dimension']),
        "sales_fact":transform_sales_fact(dfs['sales_fact'],dfs['product_dimension'])
    }
