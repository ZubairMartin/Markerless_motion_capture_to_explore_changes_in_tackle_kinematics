import cv2
import numpy as np
from typing import List
from camera import Camera
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import mpl_toolkits.mplot3d as plt3d
from mpl_toolkits.mplot3d import Axes3D

def create_3d_axes_arrows(R, T):
    # T_x, T_y, T_z: The x, y and z coordinates of the arrow locations
    T_x = np.tile(T[0],3)
    T_y = np.tile(T[1],3)
    T_z = np.tile(T[2],3)

    x = R @ np.array([[1, 0, 0]]).T.flatten()
    y = R @ np.array([[0, 1, 0]]).T.flatten()
    z = R @ np.array([[0, 0, 1]]).T.flatten()

    # u, v, w: The x, y and z components of the arrow vectors
    u = [x[0], y[0], z[0]]
    v = [x[1], y[1], z[1]]
    w = [x[2], y[2], z[2]]

    return T_x, T_y, T_z, u, v, w


def plot_cameras(ax, cameras: List[Camera]):
    T_vecs = []
    for cam in cameras:
        R, _ = cv2.Rodrigues(np.array(cam.R, dtype=float))  # convert to rotation matrix
        T = cam.T
        c = ["r", "g", "b"]
        c = np.concatenate((c, np.repeat(c, 2)))
        ax.quiver(*create_3d_axes_arrows(R.T, R.T @ (-T)), length=1, color=c)
        ax.scatter(*R.T @ (-T), label=f"{cam.name}", linewidths=1, marker='s')
        T_vecs.append(R.T @ (-T))

    T_vecs = np.array(T_vecs)
    lim = 10
    avg_x = np.mean(T_vecs[:,0])
    avg_y = np.mean(T_vecs[:,1])
    ax.set_xlim((-lim + avg_x, lim + avg_x))
    ax.set_ylim((-lim + avg_y, lim + avg_y))
    ax.set_zlim((-lim, lim))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()


def create_animation(points_3d_df, filepath, cameras=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if cameras is not None:
        plot_cameras(ax, cameras)
    graph, = ax.plot([], [], [], linestyle="", marker=".", markersize=2)
    #graph2, = ax.plot([], [], [], linestyle="", marker=".", markersize=2)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.view_init(elev=0, azim=-20) #20

    def plot_skeleton(df, ax):
        plt.cla()       # Clear previous frame scatter plots 
        plot_cameras(ax, cameras)
        ax.set_xlim3d((0,8))
        ax.set_ylim3d((-1,7))
        ax.set_zlim3d((0,8))
        
        skeleton_pairs = [
            ['ankle1','knee1'],
            ['knee1','hip1'],
            ['hip1','hip2'],
            ['hip2','knee2'],
            ['knee2','ankle2'],
            
            ['wrist1','elbow1'],
            ['elbow1','shoulder1'],
            ['shoulder1','shoulder2'],
            ['shoulder2','elbow2'],
            ['elbow2','wrist2'],
            
            ['hip1','shoulder1'],
            ['hip2','shoulder2'],

            ['chin','forehead'],
            
            ['top','upper quartile'],
            ['upper quartile','middle'],
            ['middle','lower quartile'],
            ['lower quartile','bottom'],
        ]
        for pair in skeleton_pairs:
            pts = np.array(df.loc[df['label'].isin(pair), ['x','y','z']], dtype=np.float)
            if len(pts)>1:
                line = plt3d.art3d.Line3D(pts[:,0], pts[:,1], pts[:,2])
                ax.add_line(line)
        all_pts = np.array(df[['x','y','z']], dtype=np.float)
        ax.scatter3D(all_pts[:,0], all_pts[:,1], all_pts[:,2],s=3,c='r')

    def update(frame):
        ax.view_init(elev=ax.elev+0.05, azim=ax.azim+0.02)
        ax.dist=8
        frame_points_3d_df = points_3d_df[points_3d_df['frame']==frame]
        # graph.set_data(frame_points_3d_df['x'].values, frame_points_3d_df['y'].values)
        # graph.set_3d_properties(frame_points_3d_df['z'].values)
        plot_skeleton(frame_points_3d_df, ax)
        
        return graph, #need the comma!

    
    # Distances should be equal for scaling
    ax.set_xlim3d((0,8))
    ax.set_ylim3d((-1,7))
    ax.set_zlim3d((0,8))

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = True

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.2
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.2
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.2

    frames = points_3d_df['frame'].unique().tolist()
    fps = 30
    ani = FuncAnimation(fig, update, frames=frames, blit=True, interval=1000/fps)
    mywriter = FFMpegWriter(fps=fps, codec="h264")
    ani.save(filepath, writer=mywriter, dpi=400)
    plt.close()
