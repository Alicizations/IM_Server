echo ---------------------------------------------
echo                 stop uwsgi3
echo ---------------------------------------------
cd /root/IM_Server/uwsgi_django_config
uwsgi3 --stop uwsgi.pid
echo ---------------------------------------------
echo                  git pull
echo ---------------------------------------------
cd /root/IM_Server
git pull
echo ---------------------------------------------
echo                start uwsgi3
echo ---------------------------------------------
cd /root/IM_Server/uwsgi_django_config
uwsgi3 --ini d_uwsgi.ini