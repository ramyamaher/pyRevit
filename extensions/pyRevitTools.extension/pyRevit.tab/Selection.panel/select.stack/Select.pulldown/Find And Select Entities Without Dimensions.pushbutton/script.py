"""Selects elements with no associated dimensions in current view."""

# pylint: disable=import-error,invalid-name
from pyrevit import revit, DB, HOST_APP
from pyrevit import forms
from pyrevit.compat import get_elementid_value_func

get_elementid_value = get_elementid_value_func()
doc = HOST_APP.doc

categories = {
    "Rooms": DB.BuiltInCategory.OST_Rooms,
    "Areas": DB.BuiltInCategory.OST_Areas,
    "Spaces": DB.BuiltInCategory.OST_MEPSpaces,
    "Doors": DB.BuiltInCategory.OST_Doors,
    "Windows": DB.BuiltInCategory.OST_Windows,
    "Speciality Equipment": DB.BuiltInCategory.OST_SpecialityEquipment,
    "Mechanical Equipment": DB.BuiltInCategory.OST_MechanicalEquipment,
    "Electrical Equipment": DB.BuiltInCategory.OST_ElectricalEquipment,
    "Walls": DB.BuiltInCategory.OST_Walls,
    "Curtain Walls": DB.BuiltInCategory.OST_CurtainWallPanels,
    "Ceilings": DB.BuiltInCategory.OST_Ceilings,
    "Columns": DB.BuiltInCategory.OST_StructuralColumns,
}

# make sure active view is not a sheet
if isinstance(revit.active_view, DB.ViewSheet):
    forms.alert("You're on a Sheet. Activate a model view please.", exitscript=True)

selected_switch = forms.CommandSwitchWindow.show(
    sorted(categories), message="Find undimmed elements of category:"
)

if selected_switch:
    target = categories[selected_switch]
    selection = revit.get_selection()
    all_elements = (
        DB.FilteredElementCollector(revit.doc, revit.active_view.Id)
        .OfCategory(target)
        .WhereElementIsNotElementType()
    )

    all_ids = set(get_elementid_value(x.Id) for x in all_elements)

    all_dims = (
        DB.FilteredElementCollector(revit.doc, revit.active_view.Id)
        .OfClass(DB.Dimension)
        .WhereElementIsNotElementType()
    )

    dimmed_ids = set()
    for dim in all_dims:
        for ref in dim.References:
            if HOST_APP.is_newer_than(2023):
                dimmed_ids.add(ref.ElementId.Value)
            else:
                dimmed_ids.add(ref.ElementId.IntegerValue)
    # find non dimmed
    not_dimmed_ids = all_ids.difference(dimmed_ids)
    if not_dimmed_ids:
        selection.set_to([doc.GetElement(DB.ElementId(x)) for x in not_dimmed_ids])
    else:
        forms.alert("All %s have associated dimensions." % selected_switch)
