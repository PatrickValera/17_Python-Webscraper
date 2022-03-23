from distutils.log import debug
from re import I
from flask import Flask,redirect,render_template, request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search',methods=['POST'])
def search():
    query=request.form['query']
    foodList=getFood(query)
    return render_template('result.html',foodList=foodList)

@app.route('/recipe/<string:id>/<string:tag>',methods=['GET'])
def getRecipe(id,tag):
    url=f"https://www.allrecipes.com/recipe/{id}/{tag}"
    
    html_text = requests.get(url).text
    soup=BeautifulSoup(html_text,'lxml')
    food={}
    food['name']=soup.find('div',class_='headline-wrapper').text
    food['ingredients']=soup.find('ul',class_='ingredients-section').find_all('span',class_='ingredients-item-name elementFont__body')
    food['directions']=soup.find('ul',class_='instructions-section').find_all('div',class_='paragraph')
    print('================================')
    for direction in food['directions']:
        print(direction.text)
    print('================================')
    return render_template('recipe.html',food=food)


def getFood(query):
    url=f"https://www.allrecipes.com/search/results/?search={query}"
    html_text = requests.get(url).text
    soup=BeautifulSoup(html_text,'lxml')
    foods=soup.find_all('div',class_='component card card__recipe card__facetedSearchResult',limit=3)
    ar=[]
    for food in foods:
        current={}
        current['name']=food.find('h3',class_='card__title elementFont__resetHeading')
        current['description']=food.find('div',class_='card__summary elementFont__details--paragraphWithin margin-8-tb')
        current['rating']=food.find('span',class_='review-star-text visually-hidden')
        current['rating_count']=food.find('span',class_='ratings-count elementFont__details')
        current['imgSrc']=food.find('img')['src']
        food_link=food.find('a',class_='card__titleLink manual-link-behavior elementFont__titleLink margin-8-bottom')['href'].split('/')
        current['id']=food_link[4]
        current['tag']=food_link[5]
        print(current['tag'])
        ar.append(current)
        # print(current['link'])

    # print(foods)
    # print(name.text if name else "no name")
    # print(description.text if description else "no description")
    # print(rating.text if rating else "no rating")
    # print(rating_count.text if rating_count else "no rating count")

    return ar

if __name__=='__main__':
    app.run(debug=True)