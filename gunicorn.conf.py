# https://docs.gunicorn.org/en/stable/settings.html
# INFO ON CONFIG OPTIONS >> https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

import multiprocessing

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

errorlog =  '-'  # log to stdout
accesslog = '-' # log to stdout 

loglevel = 'info'

capture_output = True # capture stdout and stderr

timeout = 3600 # 1 hour  

workers = multiprocessing.cpu_count() * 2 + 1  # multiprocessing.cpu_count() * 2 + 1 means 2 workers per CPU

worker_class = 'sync' # 'sync' or 'gevent' - default is 'sync'
# worker_class = 'gevent' # gevent is faster than sync but not as stable

threads = 15   # concurrent threads per worker