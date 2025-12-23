from src.utils import video_utils
from src.trackers.player_tracker import PlayerTracker
from src.drawers.players_track_drawer import PlayerTracksDrawer

def main():
    
    #Read video
    video_frames = video_utils.read_video("data\\input-videos\\video_1.mp4")
    # save video
    video_utils.save_video(video_frames,"output//output_video.mp4")
    #Initialize Player Tracker
    player_tracker = PlayerTracker(model_path="models\\ball_detector_model.pt")
    # run player tracking
    run_player_tracks = player_tracker.get_object_tracks(video_frames,
                                                         read_from_stub=False,
                                                         stub_path="stubs\\player_tracks_stub.pkl")
    print(run_player_tracks)
    # draw outputs
    #initialize drawer
    player_tracker_drawer = PlayerTracksDrawer()

    # draw player tracks
    output_video_frames = player_tracker_drawer.draw(video_frames,
                                                     run_player_tracks)

    video_utils.save_video(output_video_frames,"output//output_video_tracked.mp4")


if __name__ == "__main__":
    main()