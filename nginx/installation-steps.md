
####3 - Nginx Installation
**Note:** If you already have an Nginx instance that you want to use, feel free to use that instead. Just make sure to configure Kibana so it is reachable by your Nginx server (you probably want to change the host value, in /opt/kibana/config/kibana.yml, to your Kibana server's private IP address or hostname). Also, it is recommended that you enable SSL/TLS.

  - Install Nginx and Apt-utils
    - `$ sudo apt-get install nginx apache2-utils`

  - Create an admin user and assign password to it
    - `$ sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin`

  - Now open the nginx default server block
    - `$ sudo vim /etc/nginx/sites-available/default`

  - Delete the file's contents, and paste the following code block into the file.
```
server {
  listen 80;
    server_name kibana;


  error_log   /var/log/nginx/kibana.error.log;
  access_log  /var/log/nginx/kibana.access.log;



  location / {
    rewrite ^/(.*) /$1 break;
    proxy_ignore_client_abort on;
    proxy_pass http://localhost:5601;
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header  Host $http_host;

  }
}
```


```
server {
  listen 80;
    server_name jupiterlab;


  error_log   /var/log/nginx/jupiterlab.error.log;
  access_log  /var/log/nginx/jupiterlab.access.log;



 location ~ {
rewrite ^/jupiterlab(.*)$ /$1 break;
    proxy_ignore_client_abort on;
    proxy_pass http://localhost:8888;
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header  Host $http_host;

     proxy_http_version 1.1;
     proxy_set_header Upgrade $http_upgrade;
     proxy_set_header Connection "upgrade";
     proxy_read_timeout 86400;

  }
}

```


 - Save and exit. This configures Nginx to direct your server's HTTP traffic to the Kibana application, which is listening on `localhost:5601`.

  - Now restart Nginx to reflect your changes
    - `$ sudo service nginx restart`

  - Kibana is now accessible via your FQDN or the public IP address of your ELK Server i.e.
    - `http://elk\_server\_public\_ip/`
