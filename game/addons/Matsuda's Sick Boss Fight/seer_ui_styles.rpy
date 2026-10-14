# =============================================================================
# Ontological Seer: shared, static HUD materials.
# These cached nine-slice frames preserve the inlay at every panel size. The
# artwork is shared by Normal and Id; phase colour stays a separate live accent.
# No screen evaluation writes game state or generates new image data.
# =============================================================================
init -9 python:
    MSBF_SEER_UI_FRAMES = {
        (False, False): Frame(MSBF_SEER_ART + "panel.png", 18, 18),
        (True, False): Frame(MSBF_SEER_ART + "panel_active.png", 18, 18),
        (False, True): Frame(MSBF_SEER_ART + "command.png", 12, 12),
        (True, True): Frame(MSBF_SEER_ART + "command_active.png", 12, 12),
    }

    def msbf_seer_frame(active=False, command=False):
        return MSBF_SEER_UI_FRAMES[(bool(active), bool(command))]




style msbf_seer_reference_button is button:
    background None
    hover_background None
    padding (0, 4)

