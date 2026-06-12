from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import torch

from .model import build_model
from .pseudo_label import PseudoMaskConfig, generate_energy_mask


@dataclass(slots=True)
class Instance:
    instance_id: int
    score: float
    bbox_xyxy: tuple[float, float, float, float]
    mask_area: int
    center_xy: tuple[float, float]
    contour_xy: list[tuple[float, float]]
    mask: np.ndarray
    role: str = "candidate"
    role_name: str = "候选区域"
    module_point_xy: tuple[float, float] | None = None
    module_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "role": self.role,
            "role_name": self.role_name,
            "module_point_xy": list(self.module_point_xy) if self.module_point_xy else None,
            "module_score": self.module_score,
            "score": self.score,
            "bbox_xyxy": list(self.bbox_xyxy),
            "mask_area": self.mask_area,
            "center_xy": list(self.center_xy),
            "contour_xy": [list(p) for p in self.contour_xy],
        }


@dataclass(slots=True)
class FramePrediction:
    frame_index: int
    time_sec: float
    inference_time_ms: float
    detections: list[Instance]
    probability_mean: float
    probability_max: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_index": self.frame_index,
            "time_sec": self.time_sec,
            "inference_time_ms": self.inference_time_ms,
            "probability_mean": self.probability_mean,
            "probability_max": self.probability_max,
            "detections": [item.to_dict() for item in self.detections],
        }


def load_model(model_path: str | Path, *, device: str = "cpu") -> tuple[torch.nn.Module, dict[str, Any], torch.device]:
    target_device = _resolve_device(device)
    try:
        checkpoint = torch.load(model_path, map_location=target_device, weights_only=True)
    except TypeError:
        checkpoint = torch.load(model_path, map_location=target_device)
    model = build_model(base_channels=int(checkpoint.get("base_channels", 8)))
    model.load_state_dict(checkpoint["model_state"])
    model.to(target_device)
    model.eval()
    return model, checkpoint, target_device


@torch.no_grad()
def predict_frame(
    model: torch.nn.Module,
    checkpoint: dict[str, Any],
    device: torch.device,
    frame_bgr: np.ndarray,
    *,
    frame_index: int,
    time_sec: float,
    threshold: float,
    min_area: int,
    max_area_ratio: float,
    use_warm_gate: bool = True,
    max_instances: int = 8,
    max_aspect_ratio: float = 6.0,
    include_contours: bool = False,
) -> FramePrediction:
    original_height, original_width = frame_bgr.shape[:2]
    image_size = int(checkpoint["image_size"])
    tensor = _preprocess_bgr(frame_bgr, image_size).to(device)
    started = time.perf_counter()
    logits = model(tensor)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    prob = torch.sigmoid(logits)[0, 0].detach().cpu().numpy()
    prob = cv2.resize(prob, (original_width, original_height), interpolation=cv2.INTER_LINEAR)
    warm_gate = None
    if use_warm_gate:
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        gate_config = PseudoMaskConfig(
            min_area=max(12, min_area // 2),
            max_area_ratio=max_area_ratio,
            dominant_cluster_kernel=max(31, min(original_width, original_height) // 12),
            min_box_size=3,
            max_aspect_ratio=10.0,
            min_extent=0.02,
        )
        warm_gate = generate_energy_mask(frame_rgb, gate_config)
    instances = extract_instances(
        prob,
        threshold=threshold,
        min_area=min_area,
        max_area_ratio=max_area_ratio,
        warm_gate=warm_gate,
        max_instances=max_instances,
        max_aspect_ratio=max_aspect_ratio,
        include_contours=include_contours,
    )
    return FramePrediction(
        frame_index=frame_index,
        time_sec=time_sec,
        inference_time_ms=elapsed_ms,
        detections=instances,
        probability_mean=float(prob.mean()),
        probability_max=float(prob.max()),
    )


def extract_instances(
    prob: np.ndarray,
    *,
    threshold: float,
    min_area: int,
    max_area_ratio: float,
    warm_gate: np.ndarray | None = None,
    max_instances: int = 8,
    max_aspect_ratio: float = 6.0,
    include_contours: bool = False,
) -> list[Instance]:
    binary = (prob >= threshold).astype(np.uint8)
    if warm_gate is not None:
        binary = (binary & warm_gate.astype(np.uint8)).astype(np.uint8)
    max_area = int(prob.size * max_area_ratio) if max_area_ratio > 0 else prob.size
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    instances: list[Instance] = []
    for component_id in range(1, count):
        area = int(stats[component_id, cv2.CC_STAT_AREA])
        if area < min_area or area > max_area:
            continue
        mask = labels == component_id
        x = int(stats[component_id, cv2.CC_STAT_LEFT])
        y = int(stats[component_id, cv2.CC_STAT_TOP])
        w = int(stats[component_id, cv2.CC_STAT_WIDTH])
        h = int(stats[component_id, cv2.CC_STAT_HEIGHT])
        aspect = max(w / max(1, h), h / max(1, w))
        if max_aspect_ratio > 0 and aspect > max_aspect_ratio:
            continue
        extent = area / max(1, w * h)
        if extent < 0.025:
            continue
        cx, cy = centroids[component_id]
        instances.append(
            Instance(
                instance_id=len(instances) + 1,
                score=float(prob[mask].mean()),
                bbox_xyxy=(float(x), float(y), float(x + w - 1), float(y + h - 1)),
                mask_area=area,
                center_xy=(float(cx), float(cy)),
                contour_xy=_contour_points(mask) if include_contours else [],
                mask=mask,
            )
        )
    instances = _split_merged_components(
        instances,
        prob=prob,
        min_area=min_area,
        max_aspect_ratio=max_aspect_ratio,
        include_contours=include_contours,
    )
    assign_instance_roles(instances, frame_shape=prob.shape)
    instances.sort(key=_instance_sort_key, reverse=True)
    if max_instances > 0:
        instances = _keep_semantic_instances(instances, max_instances=max_instances)
    for idx, instance in enumerate(instances, start=1):
        instance.instance_id = idx
    return instances


def _split_merged_components(
    instances: list[Instance],
    *,
    prob: np.ndarray,
    min_area: int,
    max_aspect_ratio: float,
    include_contours: bool,
) -> list[Instance]:
    if len(instances) < 2:
        return instances
    rough_center = _weighted_center(instances)
    center_r = _select_center_r(instances, rough_center, frame_shape=prob.shape)
    center = center_r.center_xy if center_r is not None else rough_center
    output: list[Instance] = []
    for instance in instances:
        if instance is center_r or not _is_split_candidate(instance, center=center, frame_shape=prob.shape):
            output.append(instance)
            continue
        split_masks = _split_mask_by_angle(instance.mask, center=center, min_area=min_area, frame_shape=prob.shape)
        if len(split_masks) <= 1:
            output.append(instance)
            continue
        for mask in split_masks:
            split = _instance_from_mask(
                mask,
                prob=prob,
                instance_id=len(output) + 1,
                include_contours=include_contours,
            )
            if split is None or split.mask_area < min_area:
                continue
            if max_aspect_ratio > 0 and _bbox_aspect(split.bbox_xyxy) > max_aspect_ratio:
                continue
            output.append(split)
    for idx, instance in enumerate(output, start=1):
        instance.instance_id = idx
    return output


def _is_split_candidate(
    instance: Instance,
    *,
    center: tuple[float, float],
    frame_shape: tuple[int, int],
) -> bool:
    if instance.mask_area < 1800:
        return False
    x1, y1, x2, y2 = instance.bbox_xyxy
    width = max(1.0, x2 - x1 + 1.0)
    height = max(1.0, y2 - y1 + 1.0)
    if width * height < frame_shape[0] * frame_shape[1] * 0.10:
        return False
    ys, xs = _mask_pixels(instance)
    if len(xs) == 0:
        return False
    angles = np.degrees(np.arctan2(ys - center[1], xs - center[0]))
    return _angular_span_values(angles) >= 52.0


def _split_mask_by_angle(
    mask: np.ndarray,
    *,
    center: tuple[float, float],
    min_area: int,
    frame_shape: tuple[int, int],
) -> list[np.ndarray]:
    ys, xs = np.nonzero(mask)
    if len(xs) < max(min_area * 4, 400):
        return []
    dx = xs.astype(np.float32) - center[0]
    dy = ys.astype(np.float32) - center[1]
    distances = np.sqrt(dx * dx + dy * dy)
    far_threshold = max(float(np.quantile(distances, 0.58)), min(frame_shape) * 0.10)
    far = distances >= far_threshold
    if int(far.sum()) < max(80, min_area):
        return []

    angles = (np.degrees(np.arctan2(dy, dx)) + 360.0) % 360.0
    far_angles = angles[far]
    groups = _angular_groups(far_angles)
    if len(groups) <= 1:
        return []

    centers = np.asarray([group[0] for group in groups], dtype=np.float32)
    pixel_angles = angles.astype(np.float32)
    delta = np.abs(((pixel_angles[:, None] - centers[None, :] + 180.0) % 360.0) - 180.0)
    assignments = np.argmin(delta, axis=1)

    split_masks: list[np.ndarray] = []
    for group_index in range(len(groups)):
        submask = np.zeros(mask.shape, dtype=bool)
        selected = assignments == group_index
        if int(selected.sum()) < min_area:
            continue
        submask[ys[selected], xs[selected]] = True
        submask = _clean_split_mask(submask)
        if int(submask.sum()) >= min_area:
            split_masks.append(submask)
    if len(split_masks) <= 1:
        return []
    return split_masks


def _angular_groups(angles: np.ndarray) -> list[tuple[float, float]]:
    if len(angles) == 0:
        return []
    bin_count = 72
    hist, _ = np.histogram(angles, bins=bin_count, range=(0.0, 360.0))
    hist = np.convolve(np.r_[hist[-1], hist, hist[0]], np.array([1, 2, 1]), mode="same")[1:-1]
    threshold = max(4.0, float(hist.max()) * 0.16)
    active = hist >= threshold
    if not bool(active.any()):
        return []

    groups: list[list[int]] = []
    visited = np.zeros(bin_count, dtype=bool)
    for start in range(bin_count):
        if visited[start] or not active[start]:
            continue
        group: list[int] = []
        cursor = start
        while active[cursor] and not visited[cursor]:
            visited[cursor] = True
            group.append(cursor)
            cursor = (cursor + 1) % bin_count
        groups.append(group)

    if len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == bin_count - 1:
        groups[0] = groups[-1] + groups[0]
        groups.pop()

    weighted_groups: list[tuple[float, float]] = []
    for bins in groups:
        weight = float(sum(hist[index % bin_count] for index in bins))
        if weight < max(24.0, float(hist.sum()) * 0.06):
            continue
        centers = np.asarray([(index % bin_count + 0.5) * (360.0 / bin_count) for index in bins], dtype=np.float32)
        radians = np.deg2rad(centers)
        sin_sum = float(np.sum(np.sin(radians)))
        cos_sum = float(np.sum(np.cos(radians)))
        angle = (np.degrees(np.arctan2(sin_sum, cos_sum)) + 360.0) % 360.0
        weighted_groups.append((float(angle), weight))

    weighted_groups.sort(key=lambda item: item[1], reverse=True)
    merged: list[tuple[float, float]] = []
    for angle, weight in weighted_groups:
        match_index = None
        for idx, (existing_angle, _) in enumerate(merged):
            if _angle_distance_degrees(angle, existing_angle) < 30.0:
                match_index = idx
                break
        if match_index is None:
            merged.append((angle, weight))
        else:
            existing_angle, existing_weight = merged[match_index]
            merged[match_index] = (_weighted_angle(existing_angle, existing_weight, angle, weight), existing_weight + weight)
    merged.sort(key=lambda item: item[0])
    if len(merged) <= 1:
        fallback = _fallback_angular_groups(angles)
        if len(fallback) > len(merged):
            return fallback
    return merged[:5]


def _fallback_angular_groups(angles: np.ndarray) -> list[tuple[float, float]]:
    if len(angles) < 2:
        return []
    ordered = sorted(float((angle + 360.0) % 360.0) for angle in angles)
    gaps = [ordered[idx + 1] - ordered[idx] for idx in range(len(ordered) - 1)]
    gaps.append(ordered[0] + 360.0 - ordered[-1])
    start_index = (int(np.argmax(gaps)) + 1) % len(ordered)
    unwrapped = ordered[start_index:] + [angle + 360.0 for angle in ordered[:start_index]]
    span = unwrapped[-1] - unwrapped[0]
    if span < 88.0:
        return []
    group_count = min(5, max(2, int(round(span / 68.0))))
    centers = [float(unwrapped[0] + (idx + 0.5) * span / group_count) % 360.0 for idx in range(group_count)]
    weight = float(len(angles) / group_count)
    return [(center, weight) for center in centers]


def _clean_split_mask(mask: np.ndarray) -> np.ndarray:
    kernel = np.ones((3, 3), dtype=np.uint8)
    cleaned = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(cleaned, connectivity=8)
    if count <= 2:
        return cleaned.astype(bool)
    output = np.zeros(mask.shape, dtype=np.uint8)
    order = sorted(range(1, count), key=lambda idx: int(stats[idx, cv2.CC_STAT_AREA]), reverse=True)
    for idx in order[:2]:
        output[labels == idx] = 1
    return output.astype(bool)


def _instance_from_mask(
    mask: np.ndarray,
    *,
    prob: np.ndarray,
    instance_id: int,
    include_contours: bool,
) -> Instance | None:
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return Instance(
        instance_id=instance_id,
        score=float(prob[mask].mean()),
        bbox_xyxy=(float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max())),
        mask_area=int(mask.sum()),
        center_xy=(float(xs.mean()), float(ys.mean())),
        contour_xy=_contour_points(mask) if include_contours else [],
        mask=mask,
    )


def assign_instance_roles(instances: list[Instance], *, frame_shape: tuple[int, int]) -> None:
    if not instances:
        return
    for item in instances:
        item.role = "candidate"
        item.role_name = "候选区域"
        item.module_point_xy = None
        item.module_score = 0.0

    rough_center = _weighted_center(instances)
    center_r = _select_center_r(instances, rough_center, frame_shape=frame_shape)
    if center_r is not None:
        center_r.role = "center_r"
        center_r.role_name = "中心R标"
    center = center_r.center_xy if center_r is not None else rough_center

    armor_candidates = [item for item in instances if item is not center_r and _is_armor_like(item)]
    for item in armor_candidates:
        item.module_point_xy = _module_reference_point(item, center)
        item.module_score = _module_marker_score(item, item.module_point_xy)

    active = _select_active_module(armor_candidates)
    if active is not None:
        active.role = "active_armor"
        active.role_name = "主亮装甲模块"
        for item in armor_candidates:
            if item is not active:
                item.role = "armor_module"
                item.role_name = "装甲模块"
    elif _is_fully_activated(armor_candidates, frame_shape=frame_shape, center=center):
        whole = _whole_mechanism_instance(instances)
        if whole is not None:
            instances.append(whole)
        for item in armor_candidates:
            item.role = "armor_module"
            item.role_name = "装甲模块"
    else:
        for item in armor_candidates:
            item.role = "armor_module"
            item.role_name = "装甲模块"

    for item in instances:
        if item.role == "candidate":
            item.role = "light_candidate"
            item.role_name = "能量机关灯光候选"


def _weighted_center(instances: list[Instance]) -> tuple[float, float]:
    total = sum(max(1, item.mask_area) for item in instances)
    x = sum(item.center_xy[0] * max(1, item.mask_area) for item in instances) / total
    y = sum(item.center_xy[1] * max(1, item.mask_area) for item in instances) / total
    return float(x), float(y)


def _select_center_r(
    instances: list[Instance],
    center: tuple[float, float],
    *,
    frame_shape: tuple[int, int],
) -> Instance | None:
    if len(instances) == 1:
        item = instances[0]
        return item if _is_center_like(item, frame_shape=frame_shape) else None
    candidates = [
        item
        for item in instances
        if _is_center_like(item, frame_shape=frame_shape)
    ]
    min_center_area = max(70, int(frame_shape[0] * frame_shape[1] * 0.00025))
    strong_candidates = [item for item in candidates if item.mask_area >= min_center_area]
    if not strong_candidates:
        return None
    candidates = strong_candidates
    expected_area = max(220, int(frame_shape[0] * frame_shape[1] * 0.001))
    return min(
        candidates,
        key=lambda item: _distance_sq(item.center_xy, center) + abs(item.mask_area - expected_area) * 18.0,
    )


def _is_center_like(instance: Instance, *, frame_shape: tuple[int, int]) -> bool:
    x1, y1, x2, y2 = instance.bbox_xyxy
    width = max(1.0, x2 - x1 + 1.0)
    height = max(1.0, y2 - y1 + 1.0)
    aspect = max(width / height, height / width)
    frame_area = frame_shape[0] * frame_shape[1]
    return instance.mask_area <= max(900, int(frame_area * 0.006)) and aspect <= 2.5


def _is_armor_like(instance: Instance) -> bool:
    x1, y1, x2, y2 = instance.bbox_xyxy
    width = max(1.0, x2 - x1 + 1.0)
    height = max(1.0, y2 - y1 + 1.0)
    aspect = max(width / height, height / width)
    return instance.mask_area >= 1000 and aspect <= 6.0


def _module_reference_point(instance: Instance, center: tuple[float, float]) -> tuple[float, float]:
    ys, xs = _mask_pixels(instance)
    if len(xs) == 0:
        return instance.center_xy
    dx = xs.astype(np.float32) - center[0]
    dy = ys.astype(np.float32) - center[1]
    distances = np.sqrt(dx * dx + dy * dy)
    cutoff = float(np.quantile(distances, 0.68))
    far = distances >= cutoff
    if not bool(far.any()):
        return instance.center_xy
    return float(xs[far].mean()), float(ys[far].mean())


def _module_marker_score(instance: Instance, module_point: tuple[float, float] | None) -> float:
    if module_point is None:
        return 0.0
    ys, xs = _mask_pixels(instance)
    if len(xs) == 0:
        return 0.0
    x1, y1, x2, y2 = instance.bbox_xyxy
    box_width = max(1.0, x2 - x1 + 1.0)
    box_height = max(1.0, y2 - y1 + 1.0)
    radius = max(10.0, min(64.0, min(box_width, box_height) * 0.38))
    dx = xs.astype(np.float32) - module_point[0]
    dy = ys.astype(np.float32) - module_point[1]
    distances = np.sqrt(dx * dx + dy * dy)
    inner_radius = radius * 0.52
    mid_radius = radius * 0.95
    inner = distances <= inner_radius
    mid = (distances > inner_radius) & (distances <= mid_radius)
    inner_area = np.pi * inner_radius * inner_radius
    mid_area = np.pi * (mid_radius * mid_radius - inner_radius * inner_radius)
    inner_density = float(inner.sum() / max(1.0, inner_area))
    mid_density = float(mid.sum() / max(1.0, mid_area))
    return inner_density + 0.35 * max(0.0, inner_density - mid_density)


def _mask_pixels(instance: Instance) -> tuple[np.ndarray, np.ndarray]:
    x1, y1, x2, y2 = [int(round(v)) for v in instance.bbox_xyxy]
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(instance.mask.shape[1] - 1, x2)
    y2 = min(instance.mask.shape[0] - 1, y2)
    crop = instance.mask[y1 : y2 + 1, x1 : x2 + 1]
    ys, xs = np.nonzero(crop)
    return ys + y1, xs + x1


def _select_active_module(armor_candidates: list[Instance]) -> Instance | None:
    if not armor_candidates:
        return None
    best = max(armor_candidates, key=lambda item: item.module_score)
    if best.module_score < 0.78:
        return None
    sorted_scores = sorted((item.module_score for item in armor_candidates), reverse=True)
    if len(sorted_scores) >= 2 and sorted_scores[0] - sorted_scores[1] < 0.12 and sorted_scores[0] < 1.02:
        return None
    return best


def _is_fully_activated(
    armor_candidates: list[Instance],
    *,
    frame_shape: tuple[int, int],
    center: tuple[float, float],
) -> bool:
    if len(armor_candidates) >= 4:
        return True
    if not armor_candidates:
        return False
    union = np.zeros(frame_shape, dtype=bool)
    for item in armor_candidates:
        union |= item.mask
    union_area_ratio = float(union.sum()) / max(1, frame_shape[0] * frame_shape[1])
    if union_area_ratio >= 0.11 and _angular_span_degrees(armor_candidates, center) >= 150.0:
        return True
    return False


def _angular_span_degrees(instances: list[Instance], center: tuple[float, float]) -> float:
    if len(instances) < 2:
        return 0.0
    angles = sorted(np.degrees(np.arctan2(item.center_xy[1] - center[1], item.center_xy[0] - center[0])) for item in instances)
    return _angular_span_values(np.asarray(angles, dtype=np.float32))


def _angular_span_values(angles: np.ndarray) -> float:
    if len(angles) < 2:
        return 0.0
    angles = sorted(float((angle + 360.0) % 360.0) for angle in angles)
    gaps: list[float] = []
    for current, nxt in zip(angles, angles[1:]):
        gaps.append(float(nxt - current))
    gaps.append(float(angles[0] + 360.0 - angles[-1]))
    return 360.0 - max(gaps)


def _whole_mechanism_instance(instances: list[Instance]) -> Instance | None:
    masks = [item.mask for item in instances if item.role != "center_r" and item.mask_area >= 1000]
    if not masks:
        return None
    union = np.zeros_like(masks[0], dtype=bool)
    for mask in masks:
        union |= mask
    ys, xs = np.nonzero(union)
    if len(xs) == 0:
        return None
    x1, y1, x2, y2 = float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max())
    score_values = [item.score for item in instances if item.mask_area >= 1000]
    return Instance(
        instance_id=len(instances) + 1,
        score=float(np.mean(score_values)) if score_values else 0.0,
        bbox_xyxy=(x1, y1, x2, y2),
        mask_area=int(union.sum()),
        center_xy=(float(xs.mean()), float(ys.mean())),
        contour_xy=[],
        mask=union,
        role="whole_mechanism",
        role_name="能量机关整体",
    )


def _distance_sq(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def _bbox_aspect(bbox_xyxy: tuple[float, float, float, float]) -> float:
    x1, y1, x2, y2 = bbox_xyxy
    width = max(1.0, x2 - x1 + 1.0)
    height = max(1.0, y2 - y1 + 1.0)
    return max(width / height, height / width)


def _angle_distance_degrees(a: float, b: float) -> float:
    return float(abs(((a - b + 180.0) % 360.0) - 180.0))


def _weighted_angle(a: float, wa: float, b: float, wb: float) -> float:
    ar = np.deg2rad(a)
    br = np.deg2rad(b)
    y = np.sin(ar) * wa + np.sin(br) * wb
    x = np.cos(ar) * wa + np.cos(br) * wb
    return float((np.degrees(np.arctan2(y, x)) + 360.0) % 360.0)


def _instance_sort_key(instance: Instance) -> tuple[int, float, int]:
    role_priority = {
        "active_armor": 4,
        "whole_mechanism": 4,
        "center_r": 3,
        "armor_module": 2,
        "light_candidate": 1,
    }.get(instance.role, 0)
    return role_priority, instance.score * max(1, instance.mask_area), instance.mask_area


def _keep_semantic_instances(instances: list[Instance], *, max_instances: int) -> list[Instance]:
    whole = next((candidate for candidate in instances if candidate.role == "whole_mechanism"), None)
    if whole is not None:
        output = [whole]
        center = next((candidate for candidate in instances if candidate.role == "center_r"), None)
        if center is not None:
            output.append(center)
        return output[:max_instances]

    required: list[Instance] = []
    for role in ("active_armor", "center_r"):
        item = next((candidate for candidate in instances if candidate.role == role), None)
        if item is not None:
            required.append(item)
    output = list(required)
    for item in instances:
        if any(item is kept for kept in output):
            continue
        output.append(item)
        if len(output) >= max_instances:
            break
    return output


def _preprocess_bgr(frame_bgr: np.ndarray, image_size: int) -> torch.Tensor:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (image_size, image_size), interpolation=cv2.INTER_AREA)
    array = resized.astype(np.float32) / 255.0
    return torch.from_numpy(array.transpose(2, 0, 1)).unsqueeze(0)


def _contour_points(mask: np.ndarray, *, max_points: int = 80) -> list[tuple[float, float]]:
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return []
    contour = max(contours, key=cv2.contourArea).reshape(-1, 2)
    if len(contour) > max_points:
        step = max(1, len(contour) // max_points)
        contour = contour[::step][:max_points]
    return [(float(x), float(y)) for x, y in contour]


def _resolve_device(name: str) -> torch.device:
    if name.startswith("cuda") and not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device(name)
