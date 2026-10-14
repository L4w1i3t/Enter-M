# Shared store imports used by Ren'Py scripts and callbacks.
# Keep these available during init; standalone Python modules own their imports.
init python:
    import random
    import datetime
    import os
    import sys
    import re
    import math
    import time
    import json
    import base64
    import hashlib
    import shutil
    import traceback
    import renpy.store as store
