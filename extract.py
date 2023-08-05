import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def get_recipes(existing_recipes):
    """
    Function that scrapes title, category, author and hyperlink for each recipe in BBC Food catalogue
    """
    recipes = []

    # letters available in BBC Food catalogue
    letters = ['a', 'b', 'c', 'd', 'e',
            'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'y', 'z']

    # iterate through each recipe catalogue by letter
    for l in letters:
        # access url
        url = f"https://www.bbc.co.uk/food/recipes/a-z/{l}/1#featured-content"
        response = requests.get(url)
        response = response.content
        soup = BeautifulSoup(response, 'html.parser')

        # get number of recipe pages
        number_recipes = soup.find('div', class_='pagination-summary gel-wrap')
        total_recipes = number_recipes.find('b')
        total_recipes = int(total_recipes.text)
        num_pages =  math.ceil(total_recipes/24) + 1

        # iterate through each page
        for i in range(1, num_pages):
            # access url
            url = f"https://www.bbc.co.uk/food/recipes/a-z/{l}/{i}#featured-content"
            response = requests.get(url)
            response = response.content
            soup = BeautifulSoup(response, 'html.parser')

            # get recipe list
            recipe_list = soup.find('div', class_="gel-layout gel-layout--equal promo-collection standard-12-promos")
            if recipe_list is not None:
                recipe_list = recipe_list.find_all('a')
            for recipe in recipe_list:
                # get hyperlink
                href = 'https://www.bbc.co.uk' + recipe.attrs['href']
                if href in [r[0] for r in existing_recipes]:
                    continue
                # get title
                title = recipe.find('h3')
                title = title.text.strip()
                # get author
                author = recipe.find('span')
                author = author.text
                author = author.partition(" ")
                author = author[2]
                # get category
                category = recipe.attrs['class'][1]
                category = category.replace('promo__','')
                # append to list
                recipes.append([title, author, category, href])
    # create dataframe
    df = pd.DataFrame(recipes, columns = ['Title', 'Author', 'Category', 'href'])
    return df

def scrape_recipe_info(url):
    """
    Function that scrapes recipe information for a single recipe URL
    """
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')

    # get recipe information
    recipe_info = soup.find('div', class_='recipe-main-info gel-layout__item gel-1/1 gel-2/3@l')
    if recipe_info is None:
        return None

    # recipe leading information
    leading_info = recipe_info.find('div', class_='recipe-leading-info')

    # get prep time
    preparation_time = leading_info.find('p', class_='recipe-metadata__prep-time')
    if preparation_time is not None:
        preparation_time = preparation_time.text.strip()
    else:
        preparation_time = ''

    # get cooking time
    cooking_time = leading_info.find('p', class_='recipe-metadata__cook-time')
    if cooking_time is not None:
        cooking_time = cooking_time.text.strip()
    else:
        cooking_time = ''

    # get servings
    servings = leading_info.find('p', class_='recipe-metadata__serving')
    if servings is not None:
        servings = servings.text.strip()
    else:
        servings = ''

    # get ingredients information
    ingredients = []
    ingredients_info = recipe_info.find('div', class_='recipe-ingredients-wrapper')
    ingredients_info = ingredients_info.find_all('ul')
    for ingredient in ingredients_info:
        ingredient_list = ingredient.find_all('li')
        for item in ingredient_list:
            ingredients.append(item.text.strip())

    # get recipe steps
    steps = []
    steps_info = recipe_info.find('ol')
    steps_info = steps_info.find_all('li')
    for s in steps_info:
        step = s.find('p').text.strip()
        steps.append(step)

    return [url, preparation_time, cooking_time, servings, ingredients, steps]

def get_recipe_information(df):
    """
    Function that scrapes recipe information for each recipe in dataframe
    """
    urls = [i for i in df['href']]
    recipes_information = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(scrape_recipe_info, urls)
        for r in results:
            if r is not None:
                recipes_information.append(r)

    df = pd.DataFrame(recipes_information, columns=['href', 'Preparation Time', 'Cooking Time', 'Servings', 'Ingredients', 'Method'])

    return df