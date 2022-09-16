import tweepy as tw
import env

cliente = tw.Client(bearer_token=env.os.environ['bearer_token'], consumer_key=env.os.environ['consumer_key'], consumer_secret=env.os.environ['consumer_secret'], access_token=env.os.environ['access_token'], access_token_secret=env.os.environ['access_token_secret'])

def busca():

    busca = cliente.search_recent_tweets(query='plano de internet', max_results=30)

    return busca
