import pandas as pd
from sqlalchemy import create_engine
from extract import get_recipes, get_recipe_information
from transform import generate_uid, create_dataframes, transform_recipes, transform_ingredients, transform_methods

def load_data_to_database():
    # Create a SQLAlchemy engine to connect to the database
    engine = create_engine('postgresql://postgres:mysecretpassword@postgres:5432/bbcdb')

    # Read existing recipe hrefs from the database
    existing_recipes = pd.read_sql('SELECT href FROM bbcfood.recipes', engine)
    existing_uuids = pd.read_sql('SELECT uuid FROM bbcfood.recipes', engine)

    # Get recipe data from the website
    print("Catalogue scraping process starting")
    df_recipes = get_recipes(existing_recipes)
    df_full_recipes = get_recipe_information(df_recipes)
    print("Catalogue scraping process completed successfully")

    # Generate a unique ID for each recipe
    generate_uid(df_recipes, existing_uuids)

    # Transform the dataframes as needed
    recipes_df, ingredients_df, methods_df = create_dataframes(df_recipes, df_full_recipes)
    transform_recipes(recipes_df)
    transform_ingredients(ingredients_df)
    transform_methods(methods_df)
    print("Data transformation process completed successfully")
    

    # Write the dataframes to the database
    recipes_df.to_sql('recipes', engine, schema='bbcfood', if_exists='append', index=False)
    ingredients_df.to_sql('ingredients', engine, schema='bbcfood', if_exists='append', index=False)
    methods_df.to_sql('methods', engine, schema='bbcfood', if_exists='append', index=False)
    print("Data loading process completed successfully")

load_data_to_database()
