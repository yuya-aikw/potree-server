# About
- Nginx を用いた [Potree](https://github.com/potree/potree) の docker 環境
# Create your project
- [PotreeConverter 2.0](https://github.com/potree/PotreeConverter) で ファイル一式(`<your potree data>`)を作成
- `template.html`をコピー&編集して`<your potree data>.html`を作成
- 配置例
~~~
<path to your project>
├── <your potree data 1>.html
├── <your potree data 2>.html
...
└── pointclouds
    ├── <your potree data 1>
    │   ├── hierarchy.bin
    │   ├── log.txt
    │   ├── metadata.json
    │   └── octree.bin
    ├── <your potree data 2>
    ...
~~~

# Edit nginx config
- `nginx/default.conf`を編集
~~~nginx/default.conf
...

# htmls of your data 
location /hoge/ {
     alias /usr/share/nginx/<your project name>/;
     # index index.html;
     autoindex on;
}

...
~~~
# How to use
~~~
git clone git@github.com:yuyaa199908/potree-server.git

cd potree-server

docker build -t potree-server .

docker run --name <your container name> -d\
 -p <your host ip>:80\
 -v "$(pwd)/nginx/default.conf":/etc/nginx/conf.d/default.conf\
 -v <path to your project>:/usr/share/nginx/<your project name>\
 potree-server
~~~ 
- Potree examples: http://<your host ip address>:<your host ip>/examples/
- Your project: http://<your host ip address>:<your host ip>/<your project name>/