from .drawers_utils import draw_ellipse, draw_traingle

class PlayerTracksDrawer:
    def __init__(self):
        pass

    def draw(self, video_frames, player_tracker):
        output_video_frames = []

        # If a PlayerTracker instance was passed, compute tracks first
        if hasattr(player_tracker, 'get_object_tracks') and callable(player_tracker.get_object_tracks):
            tracks = player_tracker.get_object_tracks(video_frames)
        else:
            tracks = player_tracker

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            # Safely get per-frame player dict (may be empty)
            player_dict = tracks[frame_num] if (isinstance(tracks, (list, tuple)) and frame_num < len(tracks)) else {}

            # Draw each player's track
            for track_id, player in player_dict.items():
                frame = draw_ellipse(frame, player['bbox'], color=(0, 255, 0))

            output_video_frames.append(frame)

        return output_video_frames        