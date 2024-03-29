import multiprocessing

bind = "127.0.0.1:8082"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "/var/tmp/gunicorn_access.log"
