# -*- coding: utf-8 -*-
import os.path as op
import pickle
from System import Int64

from pyrevit import revit, DB, HOST_APP
from pyrevit import script


logger = script.get_logger()


def iterate(mode, step_size=1):
    """Iterate over elements in memorized selection"""
    index_datafile = script.get_document_data_file("SelListPrevNextIndex", "pym")
    datafile = script.get_document_data_file("SelList", "pym")

    selection = revit.get_selection()

    if op.exists(index_datafile):
        with open(index_datafile, "rb") as f:
            idx = pickle.load(f)

        if mode == "-":
            idx = idx - step_size
        else:
            idx = idx + step_size
    else:
        idx = 0

    if op.exists(datafile):
        try:
            with open(datafile, "rb") as df:
                cursel = pickle.load(df)

            if cursel:
                if idx < 0:
                    idx = abs(idx / len(cursel)) * len(cursel) + idx
                elif idx >= len(cursel):
                    idx = idx - abs(idx / len(cursel)) * len(cursel)
                if HOST_APP.is_newer_than(2025):
                    selection.set_to([DB.ElementId(Int64(list(cursel)[idx]))])
                else:
                    selection.set_to([DB.ElementId(int(list(cursel)[idx]))])

                with open(index_datafile, "wb") as f:
                    pickle.dump(idx, f)
        except Exception as io_err:
            logger.error("Error read/write to: %s | %s", datafile, io_err)
