# About
- Nginx を用いた [Potree](https://github.com/potree/potree) の docker 環境
# Create your project
- [PotreeConverter 2.0](https://github.com/potree/PotreeConverter) で ファイル一式(`<your potree data>`)を作成
- `template.html`をコピー&編集して`<your potree data>.html`を作成
- 配置例
~~~
<path to html page dir>
├──project_A
│   └── page.html
├──project_B
│   ├── page_1.html
│   ...
│   └── page_n.html
...
~~~
~~~
<path to pointcloud data dir>
├──project_A
│   └── page
│       ├── hierarchy.bin
│       ├── log.txt
│       ├── metadata.json
│       └── octree.bin
├──project_B
│   ├── page_1
│   ...
│   └── page_n
...
~~~

# How to use
- create users and passwords for basic authentication `openssl passwd -apr1`
~~~
git clone git@github.com:yuya-aikw/potree-server.git

cd potree-server

docker build -t potree-server .

cd ./nginx/
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt \
  -subj "/C=JP/ST=Tokyo/L=Office/O=MyProject/CN=<your host ip>"
cd ../

docker run --name <your container name> -d\
 -p <your host ip>:443\
 -v $(pwd)/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro \
 -v $(pwd)/nginx/server.crt:/etc/nginx/conf.d/server.crt:ro \
 -v $(pwd)/nginx/server.key:/etc/nginx/conf.d/server.key:ro \
 -v $(pwd)/.htpasswd:/etc/nginx/.htpasswd:ro \
 -v <path to html page dir      >:/usr/share/nginx/potree/_page:ro\
 -v <path to pointcloud data dir>:/usr/share/nginx/potree/_data:ro \
 potree-server
~~~ 
- access to `http://<your host ip address>:<your host ip>/potree/_page/`
- setting reload: `docker exec <your container name> nginx -s reload`

# TODO
- 
