# Twitter-Watch

## Introduction
Our Django web application is designed to collect and update data from five different Twitter accounts every 15 minutes. The app provides a powerful tool for monitoring social media activity and analyzing trends in real-time. By collecting and analyzing data from these accounts, our app helps users to stay informed about the latest news and updates, and gain valuable insights into popular topics and trends.

In addition to collecting and updating data from these accounts, our Django app also provides a user-friendly interface for displaying the collected data.

## Technologies

#### Django platform  
#### Django REST framework
#### Python
#### Pure HTML CSS 
#### PostgreSQL 
#### snscrape
#### nltk for sentiment analysis
#### Celery - updates accounts and tweets every 15 minutes.
#### Redis cloud - (https://redis.com/redis-enterprise-cloud/overview/)
#### ElephantSQL (https://www.elephantsql.com/)
#### Vercel for deploying my project (https://vercel.com/)
    
    
    
    
## API Endpoints

1) https://twitter-watch-three.vercel.app/api/accounts/
2) https://twitter-watch-three.vercel.app/api/tweets/cathiedwood
3) https://twitter-watch-three.vercel.app/api/audience/cathiedwood/ (It works for any user in tweeter)
4) https://twitter-watch-three.vercel.app/api/sentiment/cathiedwood/ (it only works for three users)



### Installing dependencies

In order to get started, following software dependencies are required:

* python3.9
* git
* pipenv (https://github.com/pypa/pipenv)


## Database migration strategy

### Models
    this project includes two models to manage Twitter accounts and threads.
    `TwitterAccount`
    `TwitterThread`
Each change in the code that is impacting detabase schema
must be accompanied by some code responsible for keeping the database in sync.

What does it mean?

1) Everytime you change some models
    you need to run this command:

        $ python manage.py makemigrations

2) Everytime you receive some changes
   apply those changes to the database schema by running this command:

        $ python manage migrate


