#!/usr/bin/env python3
"""Synthetic regressions for Matsuda sprite semantic QA."""

from __future__ import annotations

import unittest

import numpy as np

from tools import validate_matsuda_sprites as validator


class MatsudaSemanticValidationTests(unittest.TestCase):
    def test_outer_neutral_eye_must_be_fully_replaced(self) -> None:
        base = np.zeros(
            (validator.CANVAS_HEIGHT, validator.CANVAS_WIDTH, 4), dtype=np.uint8
        )
        base[190:510, 300:660, :3] = (248, 208, 188)
        base[190:510, 300:660, 3] = 255

        # Canonical neutral eye ink extends toward x=369, matching Matsuda's
        # real outer-left-eye geometry.  Other compact features keep the
        # synthetic footprint representative of both eyes/brows/mouth.
        base[325:329, 369:431, :3] = (24, 22, 24)
        base[298:302, 490:550, :3] = (24, 22, 24)
        base[316:337, 406:422, :3] = (45, 126, 76)
        base[289:311, 514:529, :3] = (45, 126, 76)
        base[296:299, 390:438, :3] = (112, 42, 44)
        base[269:272, 492:538, :3] = (112, 42, 44)
        base[390:394, 463:510, :3] = (118, 55, 52)

        footprint = validator.neutral_feature_footprint(base)
        self.assertTrue(footprint[326, 369], "outer eye was not extracted")

        complete_alpha = np.zeros(base.shape[:2], dtype=np.uint8)
        complete_alpha[footprint] = 255
        self.assertEqual(int(np.count_nonzero(footprint & (complete_alpha != 255))), 0)

        cropped_alpha = complete_alpha.copy()
        cropped_alpha[323:332, 367:379] = 0
        uncovered = footprint & (cropped_alpha != 255)
        self.assertGreater(int(uncovered.sum()), 0)
        self.assertIsNotNone(validator.mask_bbox(uncovered))

    def test_lower_jaw_uses_four_pixel_euclidean_inset(self) -> None:
        alpha = np.zeros((validator.CANVAS_HEIGHT, validator.CANVAS_WIDTH), np.uint8)
        alpha[200:600, 340:700] = 255
        forbidden = validator.face_jaw_boundary_zone(alpha)

        # With the foreground beginning at x=340, x=343 is four pixel centers
        # from nonopaque x=339 and is forbidden; x=344 is five away and safe.
        self.assertTrue(forbidden[400, 343])
        self.assertFalse(forbidden[400, 344])


if __name__ == "__main__":
    unittest.main()
