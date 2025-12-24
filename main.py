from src.utils import video_utils
from src.trackers.player_tracker import PlayerTracker
from src.trackers.ball_tracker import BallTracker
from src.drawers.players_track_drawer import PlayerTracksDrawer
from src.drawers.ball_tracks_drawer import BallTracksDrawer

def main():
    
    #Read video
    video_frames = video_utils.read_video("data\\input-videos\\video_1.mp4")
    
    
    #Initialize Tracker
    player_tracker = PlayerTracker(model_path="models\\ball_detector_model.pt")
    ball_tracker = BallTracker(model_path="models\\ball_detector_model.pt")
    # run trackers
    run_player_tracks = player_tracker.get_object_tracks(video_frames,
                                                         read_from_stub=True,
                                                         stub_path="stubs\\player_tracks_stub.pkl")
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                 read_from_stub=True,
                                                 stub_path="stubs\\ball_tracks_stub.pkl")
    # Remove wrong ball detections
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    #interpolate missing ball positions
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)
    # draw outputs
    #initialize drawer
    player_tracker_drawer = PlayerTracksDrawer()
    ball_tracker_drawer = BallTracksDrawer()

    # draw player tracks
    output_video_frames = player_tracker_drawer.draw(video_frames,
                                                run_player_tracks)
    # draw ball tracks
    output_video_frames = ball_tracker_drawer.draw(output_video_frames,
                                            ball_tracks)

    video_utils.save_video(output_video_frames,"output//output_video_tracked.mp4")


if __name__ == "__main__":
    main()