# https://docs.python.org/3/library/winsound.html

from winsound import *
# Play Windows exit sound.

PlaySound("LAKEY INSPIRED - Blue Boi", SND_FILENAME)



# Probably play Windows default sound, if any is registered (because
# "*" probably isn't the registered name of any sound).
# winsound.PlaySound("*", winsound.SND_ALIAS)