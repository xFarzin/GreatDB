import pybabel
import os
import subprocess
import sys

# We'll use babel to compile since we have it in requirements
# Actually, babel compile works differently. Let's use python's built-in msgfmt.py script usually found in Tools/i18n
# Or just write a small script using gettext's Msgfmt class if we can, or just use pybabel.
