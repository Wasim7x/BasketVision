from .drawers_utils import draw_ellipse,draw_traingle

class PlayerTracksDrawer:
    """
    A class responsible for drawing player tracks and ball possession indicators on video frames.

    Attributes:
        default_player_team_id (int): Default team ID used when a player's team is not specified.
        team_1_color (list): RGB color used to represent Team 1 players.
        team_2_color (list): RGB color used to represent Team 2 players.
    """
    def __init__(self,team_1_color=[255, 245, 238],team_2_color=[128, 0, 0]):
        """
        Initialize the PlayerTracksDrawer with specified team colors.

        Args:
            team_1_color (list, optional): RGB color for Team 1. Defaults to [255, 245, 238].
            team_2_color (list, optional): RGB color for Team 2. Defaults to [128, 0, 0].
        """
        self.default_player_team_id = 1
        self.team_1_color=team_1_color
        self.team_2_color=team_2_color

    def draw(self,video_frames,tracks,player_assignment,ball_aquisition=None):
        """
        Draw player tracks and ball possession indicators on a list of video frames.

        Args:
            video_frames (list): A list of frames (as NumPy arrays or image objects) on which to draw.
            tracks (list): A list of dictionaries where each dictionary contains player tracking information
                for the corresponding frame.
            player_assignment (list): A list of dictionaries indicating team assignments for each player
                in the corresponding frame.

        Returns:
            list: A list of frames with player tracks and ball possession indicators drawn on them.
        """

        output_video_frames= []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks[frame_num]

            player_assignment_for_frame = player_assignment[frame_num]

            # Draw Players
            for track_id, player in player_dict.items():
                team_id = player_assignment_for_frame.get(track_id,self.default_player_team_id)

                if team_id == 1:
                    color = self.team_1_color
                else:
                    color = self.team_2_color

                frame = draw_ellipse(frame, player["bbox"],color, track_id)

            output_video_frames.append(frame)

        return output_video_frames
        