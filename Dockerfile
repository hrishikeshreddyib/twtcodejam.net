FROM python:3.7-buster

RUN apt-get update && apt-get install nginx -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /app

RUN mkdir -p /app/pip_cache

COPY requirements.txt start-server.sh /app/
COPY . /app/

WORKDIR /app
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /app
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["sh","start-server.sh"]