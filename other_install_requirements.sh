sudo apt-get install python-enchant
import nltk
nltk.download('wordnet')
sudo apt install redis
sudo apt install rabbitmq-server

server {
    server_name vizvasrj.com www.vizvasrj.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/vizvasrj/MultiAuthorBlog;
    }

    location /media/ {
        root /home/vizvasrj/MultiAuthorBlog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    # listen 443 ssl; # managed by Certbot
    # ssl_certificate /etc/letsencrypt/live/vizvasrj.com/fullchain.pem; # managed by Certbot
    # ssl_certificate_key /etc/letsencrypt/live/vizvasrj.com/privkey.pem; # managed by Certbot
    # include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    # ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
# server {
#     if ($host = vizvasrj.com) {
#         return 301 https://$host$request_uri;
#     } # managed by Certbot


#     listen 80;
#     server_name vizvasrj.com www.vizvasrj.com;
#     return 404; # managed by Certbot


# }


