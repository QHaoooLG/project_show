from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

import numpy as np

from .infer import Instance


@dataclass(slots=True)
class TrackingState:
    mechanism_center: tuple[float, float] | None
    active_module_center: tuple[float, float] | None
    fitted_radius: float | None
    module_angle_deg: float | None
    angular_velocity_deg_s: float | None
    fit_error_px: float | None
    best_score: float
    best_area: int
    module_count: int
    whole_detected: bool
    module_status: str
    module_status_name: str

    def to_dict(self) -> dict:
        return {
            "mechanism_center": list(self.mechanism_center) if self.mechanism_center else None,
            "active_module_center": list(self.active_module_center) if self.active_module_center else None,
            "fitted_radius": self.fitted_radius,
            "module_angle_deg": self.module_angle_deg,
            "angular_velocity_deg_s": self.angular_velocity_deg_s,
            "fit_error_px": self.fit_error_px,
            "best_score": self.best_score,
            "best_area": self.best_area,
            "module_count": self.module_count,
            "whole_detected": self.whole_detected,
            "module_status": self.module_status,
            "module_status_name": self.module_status_name,
        }


class EnergyTracker:
    """Temporal module-parameter estimator.

    The circle fit follows the same residual form used in a typical Ceres
    Solver problem: residual_i = ||point_i - center|| - radius.
    """

    def __init__(self, *, history_size: int = 8) -> None:
        self.history: deque[tuple[float, tuple[float, float], tuple[float, float]]] = deque(maxlen=history_size)

    def update(self, instances: list[Instance], *, time_sec: float, frame_shape: tuple[int, int, int]) -> TrackingState:
        modules = [item for item in instances if item.role in {"active_armor", "armor_module"}]
        whole = next((item for item in instances if item.role == "whole_mechanism"), None)
        active = next((item for item in instances if item.role == "active_armor"), None)
        center_r = next((item for item in instances if item.role == "center_r"), None)

        if not instances:
            self.history.clear()
            return TrackingState(None, None, None, None, None, None, 0.0, 0, 0, False, "no_detection", "未检测到能量机关")

        module_points = [_module_point(item) for item in modules]
        initial_center = _initial_center(instances, center_r=center_r, whole=whole)
        fit = _fit_circle_ceres_style(module_points, initial_center=initial_center)
        mechanism_center = fit.center or initial_center
        active_center = _module_point(active) if active is not None else None
        module_angle = _angle_degrees(mechanism_center, active_center) if active_center is not None else None

        angular_velocity = None
        if active_center is not None:
            self._reset_on_unstable_jump(time_sec, mechanism_center, active_center)
            self.history.append((time_sec, mechanism_center, active_center))
            angular_velocity = self._angular_velocity()
        else:
            self.history.clear()

        status, status_name = _module_status(active=active, whole=whole, modules=modules)
        return TrackingState(
            mechanism_center=mechanism_center,
            active_module_center=active_center,
            fitted_radius=fit.radius,
            module_angle_deg=module_angle,
            angular_velocity_deg_s=math.degrees(angular_velocity) if angular_velocity is not None else None,
            fit_error_px=fit.error_px,
            best_score=active.module_score if active is not None else 0.0,
            best_area=active.mask_area if active is not None else 0,
            module_count=len(modules),
            whole_detected=whole is not None,
            module_status=status,
            module_status_name=status_name,
        )

    def _angular_velocity(self) -> float | None:
        if len(self.history) < 2:
            return None
        first = self.history[0]
        last = self.history[-1]
        dt = last[0] - first[0]
        if dt <= 1e-6:
            return None
        angle_first = _angle(first[1], first[2])
        angle_last = _angle(last[1], last[2])
        delta = _wrap_angle(angle_last - angle_first)
        return delta / dt

    def _reset_on_unstable_jump(
        self,
        time_sec: float,
        center: tuple[float, float],
        module_point: tuple[float, float],
    ) -> None:
        if not self.history:
            return
        last_time, last_center, last_point = self.history[-1]
        dt = time_sec - last_time
        if dt <= 1e-6:
            return
        angle_delta = abs(_wrap_angle(_angle(center, module_point) - _angle(last_center, last_point)))
        max_allowed = math.radians(min(110.0, max(35.0, 260.0 * dt)))
        if angle_delta > max_allowed:
            self.history.clear()


@dataclass(slots=True)
class CircleFit:
    center: tuple[float, float] | None
    radius: float | None
    error_px: float | None


def _fit_circle_ceres_style(
    points: list[tuple[float, float]],
    *,
    initial_center: tuple[float, float] | None,
) -> CircleFit:
    if not points:
        return CircleFit(initial_center, None, None)
    if len(points) == 1:
        if initial_center is None:
            return CircleFit(points[0], None, None)
        radius = _distance(initial_center, points[0])
        return CircleFit(initial_center, radius, 0.0)

    array = np.asarray(points, dtype=np.float64)
    if initial_center is None:
        center = array.mean(axis=0)
    else:
        center = np.asarray(initial_center, dtype=np.float64)
    distances = np.linalg.norm(array - center, axis=1)
    radius = float(np.median(distances))
    initial_center_array = center.copy()
    initial_radius = radius
    initial_error = _circle_error(array, center, radius)

    for _ in range(5):
        dx = center[0] - array[:, 0]
        dy = center[1] - array[:, 1]
        distances = np.maximum(np.sqrt(dx * dx + dy * dy), 1e-6)
        residual = distances - radius
        jacobian = np.column_stack((dx / distances, dy / distances, -np.ones_like(distances)))
        normal = jacobian.T @ jacobian + np.eye(3) * 1e-6
        step = np.linalg.solve(normal, -(jacobian.T @ residual))
        center += step[:2]
        radius += float(step[2])
        if float(np.linalg.norm(step)) < 1e-3:
            break

    residual = np.linalg.norm(array - center, axis=1) - radius
    error = float(np.sqrt(np.mean(residual * residual))) if len(residual) else 0.0
    center_shift = float(np.linalg.norm(center - initial_center_array))
    if (
        not np.isfinite(error)
        or not np.isfinite(radius)
        or abs(radius) > 1000.0
        or center_shift > max(180.0, initial_radius * 2.4)
        or error > initial_error + 45.0
    ):
        return CircleFit((float(initial_center_array[0]), float(initial_center_array[1])), float(abs(initial_radius)), initial_error)
    return CircleFit((float(center[0]), float(center[1])), float(abs(radius)), error)


def _circle_error(array: np.ndarray, center: np.ndarray, radius: float) -> float:
    residual = np.linalg.norm(array - center, axis=1) - radius
    return float(np.sqrt(np.mean(residual * residual))) if len(residual) else 0.0


def _initial_center(
    instances: list[Instance],
    *,
    center_r: Instance | None,
    whole: Instance | None,
) -> tuple[float, float] | None:
    if center_r is not None:
        return center_r.center_xy
    if whole is not None:
        return whole.center_xy
    meaningful = [item for item in instances if item.role in {"active_armor", "armor_module"}]
    return _weighted_center(meaningful or instances)


def _weighted_center(instances: list[Instance]) -> tuple[float, float]:
    total = sum(max(1, item.mask_area) for item in instances)
    cx = sum(item.center_xy[0] * max(1, item.mask_area) for item in instances) / total
    cy = sum(item.center_xy[1] * max(1, item.mask_area) for item in instances) / total
    return float(cx), float(cy)


def _module_point(instance: Instance | None) -> tuple[float, float] | None:
    if instance is None:
        return None
    return instance.module_point_xy or instance.center_xy


def _module_status(
    *,
    active: Instance | None,
    whole: Instance | None,
    modules: list[Instance],
) -> tuple[str, str]:
    if whole is not None:
        return "whole_mechanism", "能量机关整体"
    if active is not None:
        return "active_module", "主亮装甲模块"
    if modules:
        return "modules_only", "装甲模块"
    return "center_only", "中心标识"


def _angle(center: tuple[float, float], point: tuple[float, float]) -> float:
    return math.atan2(point[1] - center[1], point[0] - center[0])


def _angle_degrees(center: tuple[float, float], point: tuple[float, float] | None) -> float | None:
    if point is None:
        return None
    return math.degrees(_angle(center, point))


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _wrap_angle(angle: float) -> float:
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle
