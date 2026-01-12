from src.utils import video_utils
from src.trackers.player_tracker import PlayerTracker
from src.trackers.ball_tracker import BallTracker
from src.drawers.players_track_drawer import PlayerTracksDrawer
from src.drawers.ball_tracks_drawer import BallTracksDrawer
from src.drawers.team_ball_control_drawer import TeamBallControlDrawer
from src.team_assigner.team_assigner import TeamAssigner
from src.ball_aquisition.ball_aquisition_detector import BallAquisitionDetector
from src.pass_and_interception_detector.pass_and_interception_detector import PassAndInterceptionDetector
from src.drawers.pass_interception_drawer import PassInterceptionDrawer
from src.court_keypoint_detector.court_keypoint_detector import CourtKeypointDetector
from src.drawers.court_keypoint_drawer import CourtKeypointDrawer
from src.tactical_veiw_convertor.tactical_view_convertor import TacticalViewConverter
from src.drawers.tactical_view_drawer import TacticalViewDrawer
def main():
    
    #Read video
    video_frames = video_utils.read_video("D:\\project\\BasketVision\\data\\input-videos\\video_3.mp4")
    
    #Initialize Tracker
    player_tracker = PlayerTracker(model_path="models\\ball_detector_model.pt")
    ball_tracker = BallTracker(model_path="models\\ball_detector_model.pt")
    court_keypoint_detector = CourtKeypointDetector(model_path="models\\court_keypoint_detection.pt")
    
    # run trackers
    player_tracks = player_tracker.get_object_tracks(video_frames,
                                                         read_from_stub=True,
                                                         stub_path="stubs\\player_tracks_stub.pkl")
    
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                 read_from_stub=True,
                                                 stub_path="stubs\\ball_tracks_stub.pkl")
    
    court_keypoint = court_keypoint_detector.get_court_keypoints(video_frames,
                                                                read_from_stub=True,
                                                                stub_path="stubs\\court_keypoints_stub.pkl")
 
    # Remove wrong ball detections
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    #interpolate missing ball positions
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)
    # assign player teams
    team_assigner = TeamAssigner()
    player_assigment = team_assigner.get_player_teams_across_frames(video_frames,
                                                        player_tracks,
                                                        read_from_stub=True, 
                                                        stub_path="stubs\\player_team_assignment_stub.pkl")
    
    # detect ball aquisition
    ball_aquisition_detector = BallAquisitionDetector()
    ball_aquisition = ball_aquisition_detector.detect_ball_possession(player_tracks, ball_tracks)

    # detect passes and interceptions
    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(ball_aquisition, player_assigment)
    interceptions = pass_and_interception_detector.detect_interceptions(ball_aquisition, player_assigment)  

    # tactical view
    tactical_view_converter = TacticalViewConverter(court_image_path="D:\\project\\BasketVision\\images\\basketball_court.png")
    court_keypoint = tactical_view_converter.validate_keypoints(court_keypoint)

                                 
    # draw outputs
    #initialize drawer
    player_tracker_drawer = PlayerTracksDrawer()
    ball_tracker_drawer = BallTracksDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    pass_interception_drawer = PassInterceptionDrawer()
    court_keypoint_drawer = CourtKeypointDrawer()
    tactical_view_drawer = TacticalViewDrawer()

    # draw player tracks
    output_video_frames = player_tracker_drawer.draw(video_frames,
                                                player_tracks,
                                                player_assigment,
                                                ball_aquisition)
    # draw ball tracks
    output_video_frames = ball_tracker_drawer.draw(output_video_frames,
                                            ball_tracks)
    
    # draw team ball control
    output_video_frames = team_ball_control_drawer.draw(output_video_frames,
                                                        player_assigment,
                                                        ball_aquisition)
    
    # draw pass and interception statistics
    output_video_frames = pass_interception_drawer.draw(output_video_frames,
                                                        passes,
                                                        interceptions)
    
    # draw court keypoints
    output_video_frames = court_keypoint_drawer.draw(output_video_frames,
                                                    court_keypoint)
    
    output_video_frames = tactical_view_drawer.draw(output_video_frames,
                                                    tactical_view_converter.court_image_path,
                                                    tactical_view_converter.width,
                                                    tactical_view_converter.height,
                                                    tactical_view_converter.key_points)
    

    video_utils.save_video(output_video_frames,"output//output_video_tracked.mp4")


if __name__ == "__main__":
    main()