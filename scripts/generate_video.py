import os
import subprocess

def create_demo_video():
    # Capture multiple frames of the dashboard with agent-browser
    os.makedirs("/tmp/frames", exist_ok=True)
    
    for i in range(5):
        print(f"Capturing frame {i}...")
        subprocess.run([
            "agent-browser", "open", "https://man44.zo.space/compute-pool",
            "&&", "sleep", "2",
            "&&", "agent-browser", "screenshot", f"/tmp/frames/frame_{i}.png"
        ], shell=True)
    
    # Stitch with ffmpeg
    print("Stitching video...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "1", "-i", "/tmp/frames/frame_%d.png",
        "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
        "/home/workspace/stardance_assets/compute_pool_demo.mp4"
    ])
    print("Done!")

if __name__ == "__main__":
    create_demo_video()
