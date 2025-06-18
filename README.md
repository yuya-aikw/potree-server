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

# How to use
~~~
git clone git@github.com:yuyaa199908/potree-server.git

cd potree-server

docker build -t potree-server .

docker run --name <your container name> -d\
 -p <your host ip>:80\
 -v "$(pwd)/nginx/default.conf":/etc/nginx/conf.d/default.conf\
 -v <path to your project>:/usr/share/nginx/potree/<your project name>\
 potree-server
~~~ 
- Potree examples: http://`your host ip address`:`your host ip`/potree/examples/
- Your project: http://`your host ip address`:`your host ip`/potree/`your project name`/
# TODO
- ディレクトリ構造の配置
- index.htmlの作成
    - 名前, 日付, センサ名の管理
    - サムネの表示

