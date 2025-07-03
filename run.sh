docker run --name potree-server-test -d\
 -p 9999:80\
 -v "$(pwd)/nginx/default.conf":/etc/nginx/conf.d/default.conf\
 -v /mnt/bigdata/00_students/aichi_ucl/potree-server-data/meidai:/usr/share/nginx/potree/meidai\
 potree-server
