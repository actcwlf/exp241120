import argparse

import pyvista as pv
import numpy as np
from plyfile import PlyData


def load_anchor(ply_path):
    plydata = PlyData.read(ply_path)

    anchor = np.stack((
        np.asarray(plydata.elements[0]["x"]),
        np.asarray(plydata.elements[0]["y"]),
        np.asarray(plydata.elements[0]["z"])
    ), axis=1).astype(np.float32)

    return anchor


def get_down_sampled_anchor(res):
    prob = res / 100
    flag = np.random.uniform(size=anchor.shape[0] )
    flag = flag < prob
    mesh = pv.PolyData(anchor[flag])
    rgba = np.ones_like(anchor[flag]) * 200
    return mesh, rgba

def create_mesh(value):
    res = int(value)
    mesh, rgba = get_down_sampled_anchor(res)
    p.add_points(mesh, point_size=2, style='points', scalars=rgba, rgb=True, name='anchor')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ply_path', type=str, default='./point_clouds/yachtride.ply', help='path of anchor ply file')
    args = parser.parse_args()

    anchor = load_anchor(args.ply_path)
    mesh = pv.PolyData(anchor)
    rgba = np.ones_like(anchor) * 200

    p = pv.Plotter()
    p.add_points(mesh, point_size=2, style='points', scalars=rgba, rgb=True, name='anchor')

    p.add_slider_widget(create_mesh, [5, 100], title='Down Sampling')

    p.show_grid(
        color='gray',
        location='outer',
        grid='back',
        ticks='outside',
        xtitle='x',
        ytitle='y',
        ztitle='z',
        font_size=10,
    )

    p.camera.position = (anchor[:, 0].max() / 2, anchor[:, 1].max() / 2, -p.camera.position[2])
    p.camera.up = (0, -1, 0)
    p.show()
