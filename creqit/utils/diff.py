import json
from difflib import unified_diff

import creqit
from creqit.utils import pretty_date
from creqit.utils.data import cstr


@creqit.whitelist()
def get_version_diff(from_version: int | str, to_version: int | str, fieldname: str = "script") -> list[str]:
	before, before_timestamp = _get_value_from_version(from_version, fieldname)
	after, after_timestamp = _get_value_from_version(to_version, fieldname)

	if not (before and after):
		return ["Values not available for diff"]

	before = before.split("\n")
	after = after.split("\n")

	diff = unified_diff(
		before,
		after,
		fromfile=cstr(from_version),
		tofile=cstr(to_version),
		fromfiledate=before_timestamp,
		tofiledate=after_timestamp,
	)
	return list(diff)


def _get_value_from_version(version_name: int | str, fieldname: str):
	version = creqit.get_list("Version", fields=["data", "modified"], filters={"name": version_name})
	if version:
		data = json.loads(version[0].data)
		changed_fields = data.get("changed", [])

		# data structure of field: [fieldname, before_save, after_save]
		for field in changed_fields:
			if field[0] == fieldname:
				return field[2], str(version[0].modified)

	return None, None


@creqit.whitelist()
@creqit.validate_and_sanitize_search_inputs
def version_query(doctype, txt, searchfield, start, page_len, filters):
	version_filters = {
		"docname": filters["docname"],
		"ref_doctype": filters["ref_doctype"],
	}

	if fieldname := filters.get("fieldname"):
		# This helps filter version logs which contain changes to the field.
		version_filters["data"] = ("LIKE", f'%"{fieldname}"%')

	results = creqit.get_list(
		"Version",
		fields=["name", "modified", "owner"],
		filters=version_filters,
		limit_start=start,
		limit_page_length=page_len,
		order_by="creation desc",
	)
	return [(d.name, pretty_date(d.modified), d.modified, d.owner) for d in results]
