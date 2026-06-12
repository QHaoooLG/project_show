from __future__ import annotations

import math
import unittest

import cv2
import numpy as np

from rmvs.infer import Instance, assign_instance_roles, extract_instances
from rmvs.tracker import EnergyTracker


FRAME_SHAPE = (300, 300)
RUNE_CENTER = (150, 150)


def make_instance(mask: np.ndarray, instance_id: int) -> Instance:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        raise ValueError("empty mask")
    return Instance(
        instance_id=instance_id,
        score=0.9,
        bbox_xyxy=(float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max())),
        mask_area=int(mask.sum()),
        center_xy=(float(xs.mean()), float(ys.mean())),
        contour_xy=[],
        mask=mask.astype(bool),
    )


def center_mark(instance_id: int = 1) -> Instance:
    mask = np.zeros(FRAME_SHAPE, dtype=np.uint8)
    cv2.rectangle(mask, (141, 141), (159, 159), 1, -1)
    return make_instance(mask, instance_id)


def armor_module(angle_deg: float, instance_id: int, *, active_marker: bool = False) -> Instance:
    mask = np.zeros(FRAME_SHAPE, dtype=np.uint8)
    angle = math.radians(angle_deg)
    hx = int(round(RUNE_CENTER[0] + 92 * math.cos(angle)))
    hy = int(round(RUNE_CENTER[1] + 92 * math.sin(angle)))
    sx = int(round(RUNE_CENTER[0] + 24 * math.cos(angle)))
    sy = int(round(RUNE_CENTER[1] + 24 * math.sin(angle)))
    cv2.line(mask, (sx, sy), (hx, hy), 1, 12)
    cv2.circle(mask, (hx, hy), 28, 1, 6)
    cv2.rectangle(mask, (hx - 30, hy - 30), (hx + 30, hy + 30), 1, 4)
    if active_marker:
        cv2.circle(mask, (hx, hy), 15, 1, -1)
        cv2.circle(mask, (hx, hy), 18, 1, 4)
        cv2.circle(mask, (hx, hy), 9, 1, 3)
        cv2.circle(mask, (hx, hy), 3, 1, -1)
    return make_instance(mask, instance_id)


class ModuleParameterTest(unittest.TestCase):
    def test_selects_active_module_marker_instead_of_largest_lit_module(self) -> None:
        instances = [
            center_mark(1),
            armor_module(210, 2),
            armor_module(285, 3, active_marker=True),
            armor_module(0, 4),
            armor_module(75, 5),
        ]
        assign_instance_roles(instances, frame_shape=FRAME_SHAPE)

        active = next(item for item in instances if item.role == "active_armor")
        self.assertEqual(active.instance_id, 3)
        self.assertGreater(active.module_score, 0.78)
        self.assertIsNotNone(active.module_point_xy)
        self.assertEqual(sum(item.role == "active_armor" for item in instances), 1)

    def test_full_activation_creates_whole_mechanism(self) -> None:
        instances = [center_mark(1)] + [armor_module(angle, idx + 2) for idx, angle in enumerate([0, 72, 144, 216, 288])]
        assign_instance_roles(instances, frame_shape=FRAME_SHAPE)

        roles = [item.role for item in instances]
        self.assertIn("whole_mechanism", roles)
        self.assertNotIn("active_armor", roles)
        whole = next(item for item in instances if item.role == "whole_mechanism")
        self.assertEqual(whole.role_name, "能量机关整体")

    def test_center_mark_alone_is_not_active_module(self) -> None:
        instances = [center_mark(1)]
        assign_instance_roles(instances, frame_shape=FRAME_SHAPE)
        self.assertEqual(instances[0].role, "center_r")
        self.assertNotEqual(instances[0].role, "active_armor")

    def test_tracker_outputs_ceres_style_module_parameters(self) -> None:
        instances = [center_mark(1)] + [armor_module(angle, idx + 2) for idx, angle in enumerate([0, 72, 144, 216, 288])]
        assign_instance_roles(instances, frame_shape=FRAME_SHAPE)
        tracker = EnergyTracker()
        state = tracker.update(instances, time_sec=1.0, frame_shape=(300, 300, 3))
        self.assertEqual(state.module_status, "whole_mechanism")
        self.assertIsNotNone(state.mechanism_center)
        self.assertIsNotNone(state.fitted_radius)
        self.assertIsNotNone(state.fit_error_px)
        self.assertGreaterEqual(state.module_count, 4)

    def test_merged_lit_modules_are_split_by_angle(self) -> None:
        center = center_mark(1)
        first = armor_module(0, 2)
        second = armor_module(82, 3)
        merged = (first.mask | second.mask).astype(np.uint8)
        cv2.line(merged, (174, 150), (163, 239), 1, 9)

        prob = np.zeros(FRAME_SHAPE, dtype=np.float32)
        prob[center.mask] = 0.95
        prob[merged.astype(bool)] = 0.9
        instances = extract_instances(
            prob,
            threshold=0.5,
            min_area=60,
            max_area_ratio=0.9,
            max_instances=8,
        )

        modules = [item for item in instances if item.role in {"active_armor", "armor_module"}]
        self.assertGreaterEqual(len(modules), 2)
        max_bbox_area = max((item.bbox_xyxy[2] - item.bbox_xyxy[0] + 1) * (item.bbox_xyxy[3] - item.bbox_xyxy[1] + 1) for item in modules)
        self.assertLess(max_bbox_area, 22000)


if __name__ == "__main__":
    unittest.main()
