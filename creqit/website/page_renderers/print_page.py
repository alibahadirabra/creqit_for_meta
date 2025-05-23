import creqit
from creqit.website.page_renderers.template_page import TemplatePage


class PrintPage(TemplatePage):
	"""
	default path returns a printable object (based on permission)
	/Quotation/Q-0001
	"""

	def can_render(self):
		parts = self.path.split("/", 1)
		if len(parts) == 2:
			if creqit.db.exists("DocType", parts[0], True) and creqit.db.exists(parts[0], parts[1], True):
				return True

		return False

	def render(self):
		parts = self.path.split("/", 1)
		creqit.form_dict.doctype = parts[0]
		creqit.form_dict.name = parts[1]
		self.set_standard_path("printview")
		return super().render()
