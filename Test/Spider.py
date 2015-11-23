__author__ = 'lyc'

import urllib.request
from multiprocessing.dummy import Pool

urls = [
    'http://www.python.org',
    'http://www.python.org/about/',
    'http://www.python.org/doc/'
    # etc..
]

# Make the Pool of workers
pool = Pool(4)
# Open the urls in their own threads
# and return the results
#results = pool.map(urllib.request.urlopen, urls)
print(urllib.request.urlopen("http://www.baidu.com").read())
# close the pool and wait for the work to finish
pool.close()
pool.join()

#print(results)
