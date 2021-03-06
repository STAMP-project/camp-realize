import re

from camp_real_engine.abstract.abc_subst_realizer import ABC_subst_realizer
from camp_real_engine.model.realization import RegExpFileSubstNode
from camp_real_engine.dao.daos import FileContentCommiter
from camp_real_engine.abstract.abc_real_data_model import ABCSubstitutionNode



class RegExp(ABC_subst_realizer):

	def __init__(self, _content_commiter = None):
		self.content_commiter = _content_commiter if _content_commiter else FileContentCommiter()


	def exe_subst(self, substitution):
		if not (isinstance(substitution, ABCSubstitutionNode) and substitution.get_type() == "regexp"):
			return

		self.content_commiter.set_read_file(substitution.get_file_name())
		self.content_commiter.set_write_file(substitution.get_file_name())
		file_content = self.content_commiter.read_content()

		placement = substitution.get_placement_str()
		replacement = substitution.get_replacement_str()

		pattern = re.compile(placement)
		match = pattern.search(file_content)
		if not match:
			return
		modified_content = re.sub(pattern, replacement, file_content)

		self.content_commiter.write_content(modified_content)