from .drawers_utils import draw_ellipse,draw_traingle

class PlayerTracksDrawer:
    def __init__(self):
        pass

    def draw(self, video_frames, player_tracker):
        output_video_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = player_tracker[frame_num]  # Assuming player_tracks is a list of dicts per frame

            # Draw each player's track
            for track_id, player in player_dict.items():
                
                frame = draw_ellipse(frame, player['bbox'],(0, 0, 255), track_id)

            output_video_frames.append(frame)

        return output_video_frames        