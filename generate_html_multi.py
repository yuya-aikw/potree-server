#!/usr/bin/env python3
"""
Potree Viewer HTMLファイルを動的に生成するスクリプト
"""

from operator import index
import os
from pathlib import Path
from turtle import position
from typing import List


def generate_html(
    local_page_path: str,
    description: str,
    data_base_dir: str,
    data_subdirs: List[str],
    page_link_dir: str,
) -> None:
    """
    Potree Viewer HTMLファイルを生成する
    
    Args:
        local_page_path: 出力HTMLファイルのパス
        description: ビューワーの説明文（viewer.setDescription()に使用）
        data_base_dir: ベースディレクトリ（例: "/potree/_data/tmp"）
        data_subdirs: サブディレクトリ名のリスト
    """
    data_base_dir = data_base_dir.rstrip("/")
    data_subdirs_js = ",\n            ".join([f'"{data_subdir}"' for data_subdir in data_subdirs])
    
    html_content = f'''
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

        // add point clouds and annotations
        let baseDir = "{data_base_dir}";
        let subdirs = [{data_subdirs_js}];        
        let urls = subdirs.map(dir => `${{baseDir}}/${{dir}}/metadata.json`);
        urls.forEach((url, index) => {{
            Potree.loadPointCloud(url, subdirs[index], e => {{
                // add point cloud
                let pointcloud = e.pointcloud;
                let material = pointcloud.material;
                material.activeAttributeName = "rgba";
                material.minSize = 1;
                material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
                viewer.scene.addPointCloud(pointcloud);
                if (index === 0) {{
                    viewer.fitToScreen();
                }}
                
                // add annotation
                let elTitle = $(`
                    <span>
                        ${{subdirs[index]}}
                        <img src="${{Potree.resourcePath}}/icons/goto.svg" name="action_goto_page" class="annotation-action-icon" style="filter:  invert(1);"/>
                    </span>
                `);
                elTitle.find("img[name=action_goto_page]").click((event) => {{
                    event.stopPropagation();
                    // window.location.href = `${{page_link_dir}}/${{subdirs[index]}}.html`;
                    window.open(`${{page_link_dir}}/${{subdirs[index]}}.html`, '_blank');
                }});
                elTitle.toString = () => subdirs[index];
                let pc_anno_pos = [pointcloud.pcoGeometry.offset.x, pointcloud.pcoGeometry.offset.y, pointcloud.pcoGeometry.offset.z];
                let pc_anno_camera_pos = [pointcloud.pcoGeometry.offset.x, pointcloud.pcoGeometry.offset.y, pointcloud.pcoGeometry.offset.z + 10.0];
                let pc_anno = new Potree.Annotation({{
                    position: pc_anno_pos,
                    title: elTitle,
                    cameraPosition: pc_anno_camera_pos,
                    cameraTarget: pc_anno_pos,
                }});
                viewer.scene.annotations.add(pc_anno);
            }});
        }});
    </script>
</body>
</html>
'''

    # 出力ディレクトリが存在しない場合は作成
    output_dir = Path(local_page_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # HTMLファイルを書き込み
    with open(local_page_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated: {local_page_path}")


def auto_scan_directory(dir: str) -> List[str]:
    """
    指定されたディレクトリをスキャンして、サブディレクトリのリストを取得
    
    Args:
        dir: 実際のファイルシステム上のディレクトリパス
            
    Returns:
        サブディレクトリ名のリスト
    """
    path = Path(dir)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {dir}")
    
    subdirs = [d.name for d in path.iterdir() if d.is_dir()]
    subdirs.sort()  # アルファベット順にソート
    
    print(f"Found {len(subdirs)} subdirectories in {dir}")
    for subdir in subdirs:
        print(f"  - {subdir}")
    
    return subdirs


# 使用例
if __name__ == "__main__":
    local_data_dir = "/mnt/bigdata/00_students/aichi_ucl/potree-server-data/_data/toyotasystems/FTS_navvis_all_croped_voxel_20260116/cropped_pointcloud_notfloor/"
    subdirs = auto_scan_directory(local_data_dir)
    
    local_page_path = "/mnt/bigdata/00_students/aichi_ucl/potree-server-data/_page/toyotasystems/FTS_navvis_all_croped_voxel_20260116/all.html"
    description = "NAME, DATE, DEVICE"
    data_base_dir = "/potree/_data/toyotasystems/FTS_navvis_all_croped_voxel_20260116/cropped_pointcloud_notfloor"
    page_link_dir = "/potree/_page/toyotasystems/FTS_navvis_all_croped_voxel_20260116/cropped_pointcloud_notfloor"

    generate_html(
        local_page_path=local_page_path,
        description=description,
        data_base_dir=data_base_dir,
        data_subdirs=subdirs
        page_link_dir=page_link_dir,
    )
    print("\nDone!")