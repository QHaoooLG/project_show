from __future__ import annotations

import cv2
import numpy as np

from .infer import FramePrediction, Instance
from .tracker import TrackingState


def draw_visualization(
    frame_bgr: np.ndarray,
    prediction: FramePrediction,
    tracking: TrackingState,
    *,
    input_fps: float,
    processing_fps: float,
    threshold: float,
    min_area: int,
    max_display_instances: int = 8,
) -> np.ndarray:
    canvas = frame_bgr.copy()
    display_instances = [
        item
        for item in prediction.detections
        if item.role in {"active_armor", "armor_module", "center_r", "whole_mechanism"}
    ][:max_display_instances]

    _draw_fitted_circle(canvas, tracking)
    for instance in display_instances:
        _draw_instance(canvas, instance)

    panel = _parameter_panel(
        height=canvas.shape[0],
        prediction=prediction,
        tracking=tracking,
        input_fps=input_fps,
        processing_fps=processing_fps,
        threshold=threshold,
        min_area=min_area,
    )
    return np.hstack([canvas, panel])


def _draw_fitted_circle(image: np.ndarray, tracking: TrackingState) -> None:
    center = tracking.mechanism_center
    radius = tracking.fitted_radius
    if center is None or radius is None:
        return
    values = [center[0], center[1], radius]
    if not all(np.isfinite(value) for value in values):
        return
    if radius <= 1.0 or radius > max(image.shape[:2]) * 2.0:
        return
    center_xy = (int(round(center[0])), int(round(center[1])))
    cv2.circle(image, center_xy, int(round(radius)), (255, 170, 70), 1, cv2.LINE_AA)


def _draw_instance(image: np.ndarray, instance: Instance) -> None:
    color = _role_color(instance.role)
    x1, y1, x2, y2 = [int(v) for v in instance.bbox_xyxy]
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
    cv2.putText(
        image,
        _instance_label(instance),
        (x1, max(18, y1 - 6)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        color,
        1,
        cv2.LINE_AA,
    )


def _parameter_panel(
    *,
    height: int,
    prediction: FramePrediction,
    tracking: TrackingState,
    input_fps: float,
    processing_fps: float,
    threshold: float,
    min_area: int,
) -> np.ndarray:
    panel = np.full((height, 500, 3), (24, 26, 31), dtype=np.uint8)
    y = 30
    y = _draw_title(panel, y, "RoboMaster Energy Segmentation")
    y = _draw_section(panel, y, "RUN")
    y = _draw_kv(panel, y, "frame / time", f"{prediction.frame_index} / {prediction.time_sec:.3f}s")
    y = _draw_kv(panel, y, "fps in / proc", f"{input_fps:.1f} / {processing_fps:.1f}")
    y = _draw_kv(panel, y, "infer", f"{prediction.inference_time_ms:.1f} ms")

    y = _draw_section(panel, y + 3, "SEGMENTATION")
    y = _draw_kv(panel, y, "detections", f"{len(prediction.detections)}")
    y = _draw_kv(panel, y, "boxes", _role_counts(prediction.detections))
    y = _draw_kv(panel, y, "prob / thr / area", f"{prediction.probability_max:.3f} / {threshold:.2f} / {min_area}")

    y = _draw_section(panel, y + 3, "MODULE PARAMETERS")
    y = _draw_kv(panel, y, "status", tracking.module_status)
    y = _draw_kv(panel, y, "center", _fmt_point(tracking.mechanism_center))
    y = _draw_kv(panel, y, "module", _fmt_point(tracking.active_module_center))
    y = _draw_kv(panel, y, "radius / angle", _fmt(tracking.fitted_radius, 1) + " / " + _fmt(tracking.module_angle_deg, 1) + " deg")
    y = _draw_kv(panel, y, "omega", _fmt(tracking.angular_velocity_deg_s, 2) + " deg/s")
    y = _draw_kv(panel, y, "fit / score", _fmt(tracking.fit_error_px, 2) + f" px / {tracking.best_score:.3f}")
    _draw_kv(panel, y, "area / whole", f"{tracking.best_area} / {'yes' if tracking.whole_detected else 'no'}")
    return panel


def _draw_title(panel: np.ndarray, y: int, text: str) -> int:
    cv2.putText(panel, text, (18, y), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (245, 248, 252), 2, cv2.LINE_AA)
    return y + 30


def _draw_section(panel: np.ndarray, y: int, text: str) -> int:
    cv2.line(panel, (18, y), (482, y), (70, 76, 88), 1, cv2.LINE_AA)
    cv2.putText(panel, text, (18, y + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (116, 200, 255), 1, cv2.LINE_AA)
    return y + 30


def _draw_kv(panel: np.ndarray, y: int, key: str, value: str) -> int:
    cv2.putText(panel, key, (24, y), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (160, 170, 185), 1, cv2.LINE_AA)
    cv2.putText(panel, value, (185, y), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (232, 236, 242), 1, cv2.LINE_AA)
    return y + 18


def _fmt(value: float | None, decimals: int = 2) -> str:
    return "NA" if value is None else f"{value:.{decimals}f}"


def _fmt_point(point: tuple[float, float] | None) -> str:
    return "NA" if point is None else f"({point[0]:.1f},{point[1]:.1f})"


def _role_color(role: str) -> tuple[int, int, int]:
    if role == "active_armor":
        return (0, 255, 255)
    if role == "armor_module":
        return (80, 210, 80)
    if role == "center_r":
        return (255, 255, 255)
    if role == "whole_mechanism":
        return (255, 180, 40)
    return (180, 180, 180)


def _role_tag(role: str) -> str:
    return {
        "active_armor": "ACTIVE_ARMOR",
        "armor_module": "ARMOR",
        "center_r": "CENTER_R",
        "whole_mechanism": "WHOLE_MECHANISM",
        "light_candidate": "LIGHT",
    }.get(role, "BOX")


def _instance_label(instance: Instance) -> str:
    if instance.role == "whole_mechanism":
        return f"#{instance.instance_id} WHOLE_MECHANISM"
    if instance.role == "active_armor":
        return f"#{instance.instance_id} ACTIVE_ARMOR q={instance.module_score:.2f}"
    return f"#{instance.instance_id} {_role_tag(instance.role)} s={instance.score:.2f}"


def _role_counts(instances: list[Instance]) -> str:
    active = sum(1 for item in instances if item.role == "active_armor")
    armor = sum(1 for item in instances if item.role == "armor_module")
    center = sum(1 for item in instances if item.role == "center_r")
    whole = sum(1 for item in instances if item.role == "whole_mechanism")
    return f"active={active},armor={armor},R={center},whole={whole}"
