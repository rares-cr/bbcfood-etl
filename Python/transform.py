import pandas as pd
import uuid
import numpy as np

def generate_uid(df, existing_uuids):
    for name in df['href'].unique():
        new_uuid = uuid.uuid4()

        while new_uuid in existing_uuids:
            new_uuid = uuid.uuid4()

        df.loc[df['href'] == name, 'uuid'] = new_uuid

def create_dataframes(df1, df2):

    main_df = df1.merge(df2,how='left',on='href')
    cols = ['uuid','href', 'Title', 'Author', 'Category', 'Preparation Time', 'Cooking Time', 'Servings', 'Ingredients', 'Method']
    main_df = main_df[cols]
    main_df.columns = ['uuid','href', 'title', 'author', 'category', 'preparation_time', 'cooking_time', 'servings', 'ingredients', 'methods']

    ingredients_df = df2.merge(df1, how='left', on='href')
    ingredients_df = ingredients_df.drop(columns=['Preparation Time', 'Cooking Time', 'Servings', 'Method', 'Author', 'Category'])
    cols1 = ['uuid','href', 'Title', 'Ingredients']
    ingredients_df = ingredients_df.apply(pd.Series.explode)
    ingredients_df = ingredients_df[cols1]
    ingredients_df.columns = ['uuid', 'href', 'title', 'ingredient']

    methods_df = df2.drop(columns=['Preparation Time', 'Cooking Time', 'Servings', 'Ingredients'])

    methods_df = methods_df.apply(pd.Series.explode)

    methods_df = df2.merge(df1, how='left', on='href')
    methods_df = methods_df.drop(columns=['Preparation Time', 'Cooking Time', 'Servings', 'Ingredients', 'Author', 'Category'])
    cols2 = ['uuid','href', 'Title', 'Method']
    methods_df = methods_df.apply(pd.Series.explode)
    methods_df = methods_df[cols2]
    methods_df.columns = ['uuid', 'href', 'title', 'step']

    return main_df, ingredients_df, methods_df

def transform_recipes(df):
    df['preparation_time'].replace("", 'no preparation required', inplace=True)
    df['cooking_time'].replace("", 'no cooking required', inplace=True)

def transform_ingredients(df):
    df['ingredient'].replace("", np.nan, inplace=True)
    df.dropna(subset=['ingredient'], inplace=True)

def transform_methods(df):
    df['step'].replace("", np.nan, inplace=True)
    df.dropna(subset=['step'], inplace=True)
