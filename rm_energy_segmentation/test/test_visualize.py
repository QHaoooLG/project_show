from __future__ import annotations

import unittest

import numpy as np

from rmvs.infer import FramePrediction
from rmvs.tracker import TrackingState
from rmvs.visualize import draw_visualization


class VisualizationTest(unittest.TestCase):
    def test_draws_realtime_fitted_circle_from_tracking_state(self) -> None:
        frame = np.zeros((120, 160, 3), dtype=np.uint8)
        prediction = FramePrediction(
            frame_index=1,
            time_sec=0.1,
            inference_time_ms=2.0,
            detections=[],
            probability_mean=0.1,
            probability_max=0.9,
        )
        tracking = TrackingState(
            mechanism_center=(80.0, 60.0),
            active_module_center=None,
            fitted_radius=35.0,
            module_angle_deg=None,
            angular_velocity_deg_s=None,
            fit_error_px=0.0,
            best_score=0.0,
            best_area=0,
            module_count=0,
            whole_detected=False,
            module_status="center_only",
            module_status_name="中心标识",
        )

        output = draw_visualization(
            frame,
            prediction,
            tracking,
            input_fps=30.0,
            processing_fps=25.0,
            threshold=0.35,
            min_area=25,
        )

        video_region = output[:, : frame.shape[1]]
        self.assertTrue(np.any(video_region != 0))


if __name__ == "__main__":
    unittest.main()
