import cv2
import time 
import threading
import pygame


def build_as_video(self,
                       filename: str,
                       fps: int = 30,
                       record_seconds: float = 10,
                       quality: str | float = 1.0):
        """
        Record the live display to `filename` for `record_seconds` seconds at `fps`.
        `quality` may be:
          - a float scale factor (e.g. 0.5, 1.0, 2.0),
          - or one of: "4k", "2k", "1080p", "720p".
        The on-screen window size is NOT changed.
        Returns the Thread object so you can join() it before exiting.

        Example: record_th = build_as_video(scene, "gameplay_4k.mp4", fps=60, record_seconds=12, quality="4k")
        then: record_th.join()
        """
        # 1) Determine output size
        orig_w, orig_h = self.screen.get_size()

        if isinstance(quality, str):
            presets = {"4k": 2160, "2k": 1440, "1080p": 1080, "720p": 720}
            key = quality.lower()
            if key not in presets:
                raise ValueError(f"Unknown quality preset {quality!r}")
            target_h = presets[key]
            scale = target_h / orig_h
            out_h = target_h
            out_w = int(orig_w * scale)

        elif isinstance(quality, (int, float)):
            if quality <= 0:
                raise ValueError("Quality scale factor must be > 0")
            scale = float(quality)
            out_w = int(orig_w * scale)
            out_h = int(orig_h * scale)

        else:
            raise TypeError("quality must be a preset string or a numeric scale")

        # 2) Open VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, fps, (out_w, out_h))
        if not writer.isOpened():
            raise IOError(f"Could not open video writer for {filename!r}")

        stop_time = time.time() + record_seconds

        def _record_loop():
            try:
                interval = 1.0 / fps
                while time.time() < stop_time:
                    surf = pygame.display.get_surface()
                    if surf:
                        # grab pixels, transpose to H×W×C, convert to BGR
                        frame = pygame.surfarray.array3d(surf).transpose(1, 0, 2)
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        # resize only for the video output
                        if (frame.shape[1], frame.shape[0]) != (out_w, out_h):
                            frame = cv2.resize(frame, (out_w, out_h))
                        writer.write(frame)
                    time.sleep(interval)
            finally:
                writer.release()
                print(f"[Scene] Finished recording → {filename}")

        # 3) Launch the thread (non-daemon) and return it
        thread = threading.Thread(target=_record_loop)
        thread.start()
        return thread