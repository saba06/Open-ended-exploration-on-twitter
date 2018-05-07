"""
collect.py
"""
import requests
from pprint import pprint
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI
from collections import defaultdict

consumer_key = 'YkW50XXRsPpdC8EcFATtWOjC0'
consumer_secret = 'DX735dnKwS4n2TyVKOnv28RbgbOgggw6IIZklJvuwGZnB9Ny8I'
access_token = '770665274353692672-EIzNEmo8AoMH8FGhUE16LMVlOEe49dz'
access_token_secret = 'k7uFg6cMmrhidEvZ4yQnolsBdL9h3YLqvSHaxTyZcsc3q'

def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 5 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 1)

def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.

    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.

    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')

    """
    ##TODO
    f = open(filename,'r')
    return f.read().split()

def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)

    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup

    In this example, I test retrieving two users: twitterapi and twitter.

    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    ###TODO
    users = defaultdict(list)
    for name in screen_names:
        users['screen_name'].append(name)
    return robust_request(twitter,'users/lookup',users)

def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids

    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.

    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.

    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.

    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> len(get_friends(twitter, 'HillaryClinton'))
    
    """
    ###TODO
    request  = robust_request(twitter,'friends/ids',{'screen_name': screen_name})
    friends = [r for r in request]
    return friends

def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.

    Store the result in each user's dict using a new key called 'friends'.

    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing

    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    for u in users:
        u['friends'] = get_friends(twitter,u['screen_name'])

def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter

    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    c = Counter()
    for u in users:
        c.update(u['friends'])
    return c

def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.

    Args:
        users...The list of user dicts.

    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.

    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO
    l = []
    for i in range(0,len(users)):
        for j in range(i+1,len(users)):
            l.append((users[i]['screen_name'],users[j]['screen_name'],len(set(users[i]['friends']).intersection(users[j]['friends']))))
    return sorted(l)

def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    for u in users:
        print("%s %d"% (u['screen_name'],len(u['friends'])))

    
def save_graph_data(graph):
    """saves the newly created graph
    >>> graph = nx.Graph()
    >>> graph.add_nodes_from([1,2,3,4,5,6,7])
    >>> graph.add_edges_from([(1,2),(4,2),(6,4),(2,7),(3,1),(3,7)])
    >>> nx.draw(graph)
    >>> save_graph_data(graph)
    
    """
    f = open('network.txt','w+')
    f.write('node_list:'+str(graph.nodes())+'\n'+'edge_list:'+str(graph.edges())
    +'\n'+'Number of users collected:'+str(len(graph.nodes())))
    f.close()
    
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def get_names(f):
    """
    >>> f = [36008570, 18766459, 335534204, 49204865, 44039298]
    >>> get_names(f)
    {49204865: 'Brooke Baldwin', 36008570: 'Jessie J', 18766459: 'Tour', 335534204: 'John Mayer', 44039298: 'Seth Meyers'}
    """
    names = {}
    if len(f)>100:
        f_list = list(chunks(f,100))
        index= 0
        for index in range(len(f_list)):
            request = robust_request(get_twitter(),'users/lookup',{'user_id':f_list[index]})
            for node in request:
                names[node['id']]=''.join([i if ord(i) < 128 else '' for i in node['name']])
    else :
        request = robust_request(get_twitter(),'users/lookup',{'user_id':f})
        for node in request:
            names[node['id']]=''.join([i if ord(i) < 128 else '' for i in node['name']])
    return names
        
def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)

        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    graph = nx.Graph()
    graph.add_nodes_from([u['screen_name'] for u in users])
    f = [key for key,value in friend_counts.items() if value>1]
    names =get_names(f)
    graph.add_nodes_from(names.values())
    for u in users:
        graph.add_edges_from([(u['screen_name'],names[id]) for id in set(f).intersection(u['friends'])])
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    
    f=open('people_of_intrest.txt','r')
    lb = {}
    for line in f:
        line =line.rstrip()
        lb[line]=line
    f.close()    
    
    nx.draw_networkx(graph,node_size=50,node_color='r',labels=lb)
    plt.axis('off')
    plt.show()
    plt.savefig("network.png")
    save_graph_data(graph)
    
def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('people_of_intrest.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    #print('Friend Overlap:\n%s' % str(friend_overlap(users)))

    create_graph(users, friend_counts)
    
    #for classify
    males_url = 'http://www2.census.gov/topics/genealogy/' + \
            '1990surnames/dist.male.first'
    females_url = 'http://www2.census.gov/topics/genealogy/' + \
              '1990surnames/dist.female.first'
    males = requests.get(males_url).text.split('\n')
    females = requests.get(females_url).text.split('\n')
    male_names = set([m.split()[0].lower() for m in males if m])
    female_names = set([f.split()[0].lower() for f in females if f])
    
    f = open('names.txt','w')
    f.write('male:'+str(list(male_names))+'\n'+'female:'+str(list(female_names)))
    f.close()
if __name__ == '__main__':
    main()
