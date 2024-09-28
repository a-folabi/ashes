import ashes_fg as af
from ashes_fg.examples import test2, ors_buffer

af.fpaa.compile(ors_buffer, project_name='ors_buffer', chip_num=13)
