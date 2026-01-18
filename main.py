import os
import sys
import argparse
from src.logger import logging
from src.exception import MyException
from src.utils import video_utils
from src.trackers.player_tracker import PlayerTracker
from src.trackers.ball_tracker import BallTracker
from src.team_assigner.team_assigner import TeamAssigner
from src.ball_aquisition.ball_aquisition_detector import BallAquisitionDetector
from src.pass_and_interception_detector.pass_and_interception_detector import PassAndInterceptionDetector
from src.court_keypoint_detector.court_keypoint_detector import CourtKeypointDetector
from src.tactical_veiw_convertor.tactical_view_convertor import TacticalViewConverter
from src.speed_distance_calculator.speed_distance_calculator import SpeedAndDistanceCalculator
from src.utils import config_reader
from src.drawers import (
    PlayerTracksDrawer,
    BallTracksDrawer,
    TeamBallControlDrawer,
    PassInterceptionDrawer,
    CourtKeypointDrawer,        
    TacticalViewDrawer,
    SpeedAndDistanceDrawer,
)
def arg_parse():
    parser = argparse.ArgumentParser(description="Basketball Video Analysis")
    parser.add_argument(
        "--config",
        type=str,
        default="configs\\configs.yaml",
        help="Path to the configuration file",
    )
    args = parser.parse_args()
    return args

def main():
    logging.info("Starting Basketball Video Analysis Pipeline")
    config_path = arg_parse().config
    config = config_reader.load_config(config_path)
    logging.info(f"Configuration loaded from {config_path}")
    try:
        video_frames = video_utils.read_video(config["input_data_path"])
        logging.info(f"Video loaded from {config['input_data_path']} with {len(video_frames)} frames")
    except Exception as e:
        raise MyException(e, sys) from e
    
    #Initialize Tracker
    logging.info("Initializing Trackers and Detectors")
    player_tracker = PlayerTracker(model_path=config["models_dir"]["player_detector"])
    ball_tracker = BallTracker(model_path=config["models_dir"]["ball_detector"])
    court_keypoint_detector = CourtKeypointDetector(model_path=config["models_dir"]["court_keypoints_detector"])
    
    # run trackers
    logging.info("Running Player and Ball Trackers")
    player_tracks = player_tracker.get_object_tracks(video_frames,
                                                         read_from_stub=True,
                                                         stub_path="stubs\\player_tracks_stub.pkl")
    
    logging.info("Running Ball Tracker")
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                 read_from_stub=True,
                                                 stub_path="stubs\\ball_tracks_stub.pkl")
    logging.info("Running Court Keypoint Detector")
    court_keypoint = court_keypoint_detector.get_court_keypoints(video_frames,
                                                                read_from_stub=True,
                                                                stub_path="stubs\\court_keypoints_stub.pkl")
 
    # Remove wrong ball detections
    logging.info("removing wrong ball detections and interpolating missing positions")
    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    #interpolate missing ball positions
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)
    # assign player teams
    logging.info("Assigning Player Teams based on Jersey Colors")
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
    logging.info("Transforming Player Positions to Tactical View")
    tactical_view_converter = TacticalViewConverter(court_image_path="D:\\project\\BasketVision\\images\\basketball_court.png")
    court_keypoint = tactical_view_converter.validate_keypoints(court_keypoint)
    tactical_player_positions = tactical_view_converter.transform_players_to_tactical_view(court_keypoint, player_tracks)

    # speed and distance calculation
    logging.info("Calculating Player Speed and Distance Covered")
    speed_distance_calculator = SpeedAndDistanceCalculator(
                                   tactical_view_converter.width,
                                   tactical_view_converter.height,
                                   tactical_view_converter.actual_height_in_meters,
                                   tactical_view_converter.actual_width_in_meters)
    
    player_distance_per_frame = speed_distance_calculator.calculate_distance(tactical_player_positions)
    player_speed_per_frame = speed_distance_calculator.calculate_speed(player_distance_per_frame)

    
    # draw outputs
    #initialize drawer
    logging.info("initializing drawers and generating output video")
    player_tracker_drawer = PlayerTracksDrawer()
    ball_tracker_drawer = BallTracksDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()
    pass_interception_drawer = PassInterceptionDrawer()
    court_keypoint_drawer = CourtKeypointDrawer()
    tactical_view_drawer = TacticalViewDrawer()
    speed_distance_drawer = SpeedAndDistanceDrawer()

    # draw player tracks
    logging.info("Drawing Player and Ball Tracks on Video Frames")
    output_video_frames = player_tracker_drawer.draw(video_frames,
                                                player_tracks,
                                                player_assigment,
                                                ball_aquisition)
    # draw ball tracks
    logging.info("Drawing Ball Tracks on Video Frames")
    output_video_frames = ball_tracker_drawer.draw(output_video_frames,
                                                    ball_tracks)
    # draw frame number

    # draw court keypoints
    logging.info("Drawing Court Keypoints on Video Frames")
    output_video_frames = court_keypoint_drawer.draw(output_video_frames,
                                                    court_keypoint)
    
    # draw team ball control
    logging.info("Drawing Team Ball Control on Video Frames")
    output_video_frames = team_ball_control_drawer.draw(output_video_frames,
                                                        player_assigment,
                                                        ball_aquisition)
    
    # draw pass and interception statistics
    logging.info("Drawing Pass and Interception Events on Video Frames")
    output_video_frames = pass_interception_drawer.draw(output_video_frames,
                                                        passes,
                                                        interceptions)
    logging.info("Drawing Player Speed and Distance on Video Frames")
    output_video_frames = speed_distance_drawer.draw(output_video_frames,
                                                    player_tracks,
                                                    player_distance_per_frame,
                                                    player_speed_per_frame)
    
    logging.info("Drawing Tactical View on Video Frames")
    output_video_frames = tactical_view_drawer.draw(output_video_frames,
                                                    tactical_view_converter.court_image_path,
                                                    tactical_view_converter.width,
                                                    tactical_view_converter.height,
                                                    tactical_view_converter.key_points,
                                                    tactical_player_positions,
                                                    player_assigment,
                                                    ball_aquisition)
    
    video_name = os.path.splitext(os.path.basename(config["input_data_path"]))[0]
    output_path = os.path.join(config["output_dir"], f"{video_name}_output.mp4")
    video_utils.save_video(output_video_frames, output_path)
    logging.info(f"Output video saved to {output_path}")


if __name__ == "__main__":
    main()