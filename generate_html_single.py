#!/usr/bin/env python3
"""
Potree Viewer HTMLファイルを動的に生成するスクリプト
"""

import os
from pathlib import Path
from typing import List


def generate_html(
    local_page_path: str,
    description: str,
    data_path: str,
) -> None:
    """
    Potree Viewer HTMLファイルを生成する
    
    Args:
        local_page_path: 出力HTMLファイルのパス
        description: ビューワーの説明文（viewer.setDescription()に使用）
        data_path: データのパス（例: "/potree/_data/tmp"）
    """
    data_path = data_path.rstrip("/")

    html_content = '''
<!-- copyed from https://github.com/potree/potree/blob/develop/examples/viewer.html -->
<!-- changed ../ to /potree/ -->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Potree Viewer</title>

    <link rel="stylesheet" type="text/css" href="/potree/build/potree/potree.css">
    <link rel="stylesheet" type="text/css" href="/potree/libs/jquery-ui/jquery-ui.min.css">
    <link rel="stylesheet" type="text/css" href="/potree/libs/openlayers3/ol.css">
    <link rel="stylesheet" type="text/css" href="/potree/libs/spectrum/spectrum.css">
    <link rel="stylesheet" type="text/css" href="/potree/libs/jstree/themes/mixed/style.css">
</head>

<body>
    <script src="/potree/libs/jquery/jquery-3.1.1.min.js"></script>
    <script src="/potree/libs/spectrum/spectrum.js"></script>
    <script src="/potree/libs/jquery-ui/jquery-ui.min.js"></script>

    <script src="/potree/libs/other/BinaryHeap.js"></script>
    <script src="/potree/libs/tween/tween.min.js"></script>
    <script src="/potree/libs/d3/d3.js"></script>
    <script src="/potree/libs/proj4/proj4.js"></script>
    <script src="/potree/libs/openlayers3/ol.js"></script>
    <script src="/potree/libs/i18next/i18next.js"></script>
    <script src="/potree/libs/jstree/jstree.js"></script>
    <script src="/potree/build/potree/potree.js"></script>
    <script src="/potree/libs/plasio/js/laslaz.js"></script>

    <!-- INCLUDE ADDITIONAL DEPENDENCIES HERE -->
    <!-- INCLUDE SETTINGS HERE -->

    <div class="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <div id="potree_render_area"
            style="background-image: url('/potree/build/potree/resources/images/background.jpg');"></div>
        <div id="potree_sidebar_container"> </div>
    </div>

    <script type="module">
        // create viewer
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));
        viewer.setEDLEnabled(false);
        viewer.setFOV(60);
        viewer.setPointBudget(1_000_000);
        viewer.loadSettingsFromURL();
        viewer.setBackground("skybox");
        viewer.loadGUI(() => {{
            viewer.setLanguage('jp');
            $("#menu_tools").next().show();
            $("#menu_appearance").next().show();
            $("#menu_clipping").next().show();
            viewer.toggleSidebar();
        }});
        viewer.setDescription("{description}");

        // classification
        let classifications = {{}};
        for (let i = 64; i < 256; i++) {{
            classifications[i] = {{
                visible: true,
                name: String(i),
                color: [Math.random(),Math.random(),Math.random(),1.0], 
            }};
        }}
        classifications.DEFAULT = {{visible: false,name: 'default',color: [1.0, 1.0, 1.0, 1.0]}};
        viewer.setClassifications(classifications);
        
        // add point cloud
        Potree.loadPointCloud("{data_path}/metadata.json", "pointcloud", e => {{
            let pointcloud = e.pointcloud;
            let material = pointcloud.material;
            material.activeAttributeName = "rgba";
            material.minSize = 1;
            material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
            viewer.scene.addPointCloud(pointcloud);
            viewer.fitToScreen();
        }});
    </script>
</body>
</html>
'''.format(description=description, data_path=data_path)

    # 出力ディレクトリが存在しない場合は作成
    output_dir = Path(local_page_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # HTMLファイルを書き込み
    with open(local_page_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated: {local_page_path}")

# 使用例
if __name__ == "__main__":
    # local_page_path = "<path to html page dir>/hoge.html"
    # description = "NAME, DATE, DEVICE"
    # data_path = "/potree/_data/hoge"
    
    # generate_html(
    #     local_page_path=local_page_path ,
    #     description=description,
    #     data_path=data_path
    # )
    # print("\nDone!")
    
    # 1. local_data_dirを設定
    local_data_dir = "/mnt/bigdata/00_students/aichi_ucl/potree-server-data/_data/toyotasystems/FTS_navvis_all_croped_voxel_20260116/cropped_pointcloud/"
    local_page_base_dir = "/mnt/bigdata/00_students/aichi_ucl/potree-server-data/_page/toyotasystems/FTS_navvis_all_croped_voxel_20260116/cropped_pointcloud/"
    
    # 2. local_data_dir直下のディレクトリをすべて取得
    data_path_obj = Path(local_data_dir)
    if not data_path_obj.exists():
        raise FileNotFoundError(f"Directory not found: {local_data_dir}")
    
    subdirs = [d for d in data_path_obj.iterdir() if d.is_dir()]
    subdirs.sort()  # アルファベット順にソート
    
    print(f"Found {len(subdirs)} subdirectories in {local_data_dir}")
    
    # 各ディレクトリに対してHTMLを生成
    for subdir in subdirs:
        dir_name = subdir.name
        print(f"\nProcessing: {dir_name}")
        
        # 3. local_page_path = "<path to html page dir>/[ディレクトリ名].html"
        local_page_path = f"{local_page_base_dir}{dir_name}.html"
        
        # 4. data_path = "/potree/_data/[ディレクトリ名]"
        data_path = f"/potree/_data/toyotasystems/FTS_navvis_all_croped_voxel_20260116/cropped_pointcloud/{dir_name}"
        
        description = f"{dir_name}"
        
        # 5. generate_htmlに渡して実行
        generate_html(
            local_page_path=local_page_path,
            description=description,
            data_path=data_path
        )
    
    print("\nAll done!")
    