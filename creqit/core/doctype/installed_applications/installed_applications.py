# Copyright (c) 2020, creqit Technologies and contributors
# License: MIT. See LICENSE

import json

import creqit
from creqit import _
from creqit.model.document import Document


class InvalidAppOrder(creqit.ValidationError):
	pass


class InstalledApplications(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from creqit.core.doctype.installed_application.installed_application import InstalledApplication
		from creqit.types import DF

		installed_applications: DF.Table[InstalledApplication]
	# end: auto-generated types

	def update_versions(self):
		self.delete_key("installed_applications")
		for app in creqit.utils.get_installed_apps_info():
			self.append(
				"installed_applications",
				{
					"app_name": app.get("app_name"),
					"app_version": app.get("version") or "UNVERSIONED",
					"git_branch": app.get("branch") or "UNVERSIONED",
				},
			)
		self.save()


@creqit.whitelist()
def update_installed_apps_order(new_order: list[str] | str):
	"""Change the ordering of `installed_apps` global

	This list is used to resolve hooks and by default it's order of installation on site.

	Sometimes it might not be the ordering you want, so thie function is provided to override it.
	"""
	creqit.only_for("System Manager")

	if isinstance(new_order, str):
		new_order = json.loads(new_order)

	creqit.local.request_cache and creqit.local.request_cache.clear()
	existing_order = creqit.get_installed_apps(_ensure_on_bench=True)

	if set(existing_order) != set(new_order) or not isinstance(new_order, list):
		creqit.throw(
			_("You are only allowed to update order, do not remove or add apps."), exc=InvalidAppOrder
		)

	# Ensure creqit is always first regardless of user's preference.
	if "creqit" in new_order:
		new_order.remove("creqit")
	new_order.insert(0, "creqit")

	creqit.db.set_global("installed_apps", json.dumps(new_order))

	_create_version_log_for_change(existing_order, new_order)


def _create_version_log_for_change(old, new):
	version = creqit.new_doc("Version")
	version.ref_doctype = "DefaultValue"
	version.docname = "installed_apps"
	version.data = creqit.as_json({"changed": [["current", json.dumps(old), json.dumps(new)]]})
	version.flags.ignore_links = True  # This is a fake doctype
	version.flags.ignore_permissions = True
	version.insert()


@creqit.whitelist()
def get_installed_app_order() -> list[str]:
	creqit.only_for("System Manager")

	return creqit.get_installed_apps(_ensure_on_bench=True)
