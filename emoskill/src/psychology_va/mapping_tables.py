from __future__ import annotations

# This is a seed engineering table for the first runnable version of the
# pipeline. Both valence and arousal use the same 1-10 scoring convention as
# the model prompt: valence 1 = very negative, 5.5 = neutral, 10 = very positive;
# arousal 1 = very calm/deactivated, 5.5 = moderate activation, 10 = highly
# activated. Replace these coordinates with your validated PANAS-to-VA table
# if you already have a lab-approved or paper-backed mapping.
PANAS_DISCRETE_VA_MAP: dict[str, dict[str, float]] = {
    "interested": {"valence": 7.975, "arousal": 6.580},
    "excited": {"valence": 9.190, "arousal": 9.100},
    "strong": {"valence": 7.570, "arousal": 7.480},
    "enthusiastic": {"valence": 9.280, "arousal": 8.740},
    "proud": {"valence": 8.830, "arousal": 6.760},
    "alert": {"valence": 7.030, "arousal": 8.020},
    "inspired": {"valence": 9.055, "arousal": 7.030},
    "determined": {"valence": 7.795, "arousal": 7.660},
    "attentive": {"valence": 6.760, "arousal": 5.860},
    "active": {"valence": 7.390, "arousal": 8.200},
    "distressed": {"valence": 2.080, "arousal": 8.380},
    "upset": {"valence": 2.260, "arousal": 7.660},
    "guilty": {"valence": 2.440, "arousal": 5.680},
    "scared": {"valence": 1.630, "arousal": 9.280},
    "hostile": {"valence": 1.990, "arousal": 8.020},
    "irritable": {"valence": 2.620, "arousal": 7.300},
    "ashamed": {"valence": 2.170, "arousal": 5.320},
    "nervous": {"valence": 2.710, "arousal": 8.290},
    "jittery": {"valence": 2.890, "arousal": 8.920},
    "afraid": {"valence": 1.540, "arousal": 9.100},
}
