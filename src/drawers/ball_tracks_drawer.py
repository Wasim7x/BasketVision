from .drawers_utils import draw_traingle

class BallTracksDrawer:
    """
    A drawer class responsible for drawing ball tracks on video frames.

    Attributes:
        ball_pointer_color (tuple): The color used to draw the ball pointers (in BGR format).
    """

    def __init__(self):
        """
        Initialize the BallTracksDrawer instance with default settings.
        """
        self.ball_pointer_color = (0, 255, 0)

    def draw(self, video_frames, tracks):
        """
        Draws ball pointers on each video frame based on provided tracking information.

        Args:
            video_frames (list): A list of video frames (as NumPy arrays or image objects).
            tracks (list): A list of dictionaries where each dictionary contains ball information
                for the corresponding frame.

        Returns:
            list: A list of processed video frames with drawn ball pointers.
        """
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            ball_dict = tracks[frame_num]

            # Draw ball 
            for _, ball in ball_dict.items():
                if ball["bbox"] is None:
                    continue
                frame = draw_traingle(frame, ball["bbox"],self.ball_pointer_color)

            output_video_frames.append(frame)
            
        return output_video_frames