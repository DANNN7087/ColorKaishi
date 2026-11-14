from anki import hooks
import csv

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from . import wordtypes, colors

row_strings = wordtypes.data.split("\n");
rows = []
for row in row_strings:
    rows.append(row.split(","));

color_row_strings = colors.colors.split("\n");
color_rows = []
for color_row in color_row_strings:
    color_rows.append(color_row.split(","));

def backup() -> bool:
    created = mw.col.create_backup(
        backup_folder=mw.pm.backupFolder(),
        force=True,
        wait_for_completion=True,
    )
    return created

def getCardColor(index) -> str:
    type = rows[index][1]
    for row in color_rows:
        # if current rows 1st value is equal to input, print that row
        if type == row[0]:
            return row[1]
    return "N/A"

def colorCards() -> None:
    # backup
    if not backup():
        showInfo("Failed to create backup; restart Anki and try again.")

    else:
        # get kaishi cards
        ids = mw.col.find_notes("\"deck:Kaishi 1.5k\"")
        note = mw.col.get_note(ids[0])
        color_index = note.keys().index("Frequency")
        modified_notes: list["Note"] = []

        offset = 0
        id = ids[0]
        card = mw.col.get_card(id)
        note = card.note()
        word = note.fields[note.keys().index("Word")]
        if word != "私":
            offset = 1

        for i in range(1500):
            id = ids[i+offset]
            card = mw.col.get_card(id)
            note = card.note()
            word = note.fields[note.keys().index("Word")]
            note.fields[color_index] = getCardColor(i)

            modified_notes.append(note)
        mw.col.update_notes(modified_notes)

        showInfo("""Created backup, then colored %d cards in Kaishi 1.5k.

This overwrote the \"Frequency\" field.""" % (len(ids)-offset))

# create a new menu item, "test"
action = QAction("Color Kaishi", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, colorCards)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
