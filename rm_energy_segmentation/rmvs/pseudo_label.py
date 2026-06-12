from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True, slots=True)
class PseudoMaskConfig:
    min_saturation: int = 85
    min_value: int = 105
    min_area: int = 80
    max_area_ratio: float = 0.65
    close_kernel: int = 5
    open_kernel: int = 3
    bright_core_value: int = 210
    bright_core_dilate: int = 11
    dominant_cluster_kernel: int = 101
    keep_dominant_cluster: bool = True
    min_box_size: int = 4
    max_aspect_ratio: float = 9.0
    min_extent: float = 0.025


def generate_energy_mask(image_rgb: np.ndarray, config: PseudoMaskConfig | None = None) -> np.ndarray:
    cfg = config or PseudoMaskConfig()
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    red = (hue <= 12) | (hue >= 168)
    orange_yellow = (hue >= 8) & (hue <= 42)
    warm_color = (red | orange_yellow) & (sat >= cfg.min_saturation) & (val >= cfg.min_value)

    # Only keep white/yellow overexposed cores when they are adjacent to warm rune light.
    core_kernel = np.ones((max(1, cfg.bright_core_dilate), max(1, cfg.bright_core_dilate)), dtype=np.uint8)
    near_warm = cv2.dilate(warm_color.astype(np.uint8), core_kernel) > 0
    bright_core = (val >= cfg.bright_core_value) & (sat >= 25) & near_warm
    mask = (warm_color | bright_core).astype(np.uint8)

    if cfg.close_kernel > 1:
        kernel = np.ones((cfg.close_kernel, cfg.close_kernel), dtype=np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    if cfg.open_kernel > 1:
        kernel = np.ones((cfg.open_kernel, cfg.open_kernel), dtype=np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    if cfg.keep_dominant_cluster:
        mask = keep_main_light_cluster(mask, kernel_size=cfg.dominant_cluster_kernel)
    return filter_mask_components(
        mask,
        min_area=cfg.min_area,
        max_area_ratio=cfg.max_area_ratio,
        min_box_size=cfg.min_box_size,
        max_aspect_ratio=cfg.max_aspect_ratio,
        min_extent=cfg.min_extent,
    )


def keep_main_light_cluster(mask: np.ndarray, *, kernel_size: int) -> np.ndarray:
    if int(mask.sum()) == 0:
        return mask
    kernel_size = max(3, int(kernel_size))
    if kernel_size % 2 == 0:
        kernel_size += 1
    cluster_mask = cv2.dilate(mask.astype(np.uint8), np.ones((kernel_size, kernel_size), dtype=np.uint8))
    count, labels = cv2.connectedComponents(cluster_mask, connectivity=8)
    if count <= 2:
        return mask
    best_label = 0
    best_score = 0
    for label in range(1, count):
        score = int(mask[labels == label].sum())
        if score > best_score:
            best_score = score
            best_label = label
    if best_label == 0:
        return mask
    return (mask & (labels == best_label)).astype(np.uint8)


def filter_mask_components(
    mask: np.ndarray,
    *,
    min_area: int,
    max_area_ratio: float,
    min_box_size: int = 1,
    max_aspect_ratio: float = 0.0,
    min_extent: float = 0.0,
) -> np.ndarray:
    output = np.zeros(mask.shape, dtype=np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    max_area = int(mask.size * max_area_ratio) if max_area_ratio > 0 else mask.size
    for component_id in range(1, count):
        area = int(stats[component_id, cv2.CC_STAT_AREA])
        if area < min_area or area > max_area:
            continue
        width = int(stats[component_id, cv2.CC_STAT_WIDTH])
        height = int(stats[component_id, cv2.CC_STAT_HEIGHT])
        if width < min_box_size or height < min_box_size:
            continue
        aspect = max(width / max(1, height), height / max(1, width))
        if max_aspect_ratio > 0 and aspect > max_aspect_ratio:
            continue
        extent = area / max(1, width * height)
        if min_extent > 0 and extent < min_extent:
            continue
        output[labels == component_id] = 1
    return output
