from __future__ import annotations

import unittest

import cv2
import numpy as np

from rmvs.pseudo_label import PseudoMaskConfig, generate_energy_mask


class PseudoLabelTest(unittest.TestCase):
    def test_generate_energy_mask_from_bright_red_target(self) -> None:
        image = np.zeros((96, 128, 3), dtype=np.uint8)
        cv2.circle(image, (64, 48), 18, (255, 40, 30), -1)
        mask = generate_energy_mask(image, PseudoMaskConfig(min_area=20))
        self.assertEqual(mask.shape, image.shape[:2])
        self.assertGreater(int(mask.sum()), 100)

    def test_reject_green_and_blue_lights(self) -> None:
        image = np.zeros((96, 128, 3), dtype=np.uint8)
        cv2.circle(image, (32, 48), 16, (0, 255, 0), -1)
        cv2.circle(image, (92, 48), 16, (20, 80, 255), -1)
        mask = generate_energy_mask(image, PseudoMaskConfig(min_area=20))
        self.assertEqual(int(mask.sum()), 0)

    def test_keep_dominant_rune_cluster_over_small_red_reflection(self) -> None:
        image = np.zeros((160, 220, 3), dtype=np.uint8)
        cv2.circle(image, (120, 80), 28, (255, 60, 20), -1)
        cv2.rectangle(image, (125, 76), (178, 86), (255, 180, 30), -1)
        cv2.circle(image, (18, 145), 6, (255, 35, 25), -1)
        mask = generate_energy_mask(
            image,
            PseudoMaskConfig(min_area=20, dominant_cluster_kernel=45),
        )
        self.assertGreater(int(mask[60:105, 95:185].sum()), 500)
        self.assertEqual(int(mask[135:155, 5:30].sum()), 0)


if __name__ == "__main__":
    unittest.main()
