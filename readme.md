## Visualize anchors of compressed representation

Install requirements
```
pip install -r requirements.txt
```

Run visualization script

```
python vis_point_clouds.py --ply_path ./point_clouds/beauty.ply
```


## Visualize video

Install requirements
```
pip install -r requirements.txt
```

Run visualization script

```
python play_video_qt.py --video_path1 ./videos/nerv/ShakeNDry.mkv --video_path2 ./videos/gsvc/ShakeNDry.mkv
```

Press `space` to pause and replay. We include decoded sample of NeRV and GSVC in `videos/nerv` and `videos/gsvc` respectively.
