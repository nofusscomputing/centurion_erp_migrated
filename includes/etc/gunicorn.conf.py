
access_logfile = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({x-forwarded-for}i)s"'

bind = 'unix:/run/gunicorn.sock'

forwarded_allow_ips = "*"
forwarder_headers = "X-REAL-IP,X-FORWARDED-FOR,X-FORWARDED-PROTO"

workers = 10
