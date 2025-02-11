import ashes_fg as af
from ashes_fg.examples import c4_offchip, cs_amp, ors_buffer, test2

af.fpaa.compile(ors_buffer, project_name='ors_buffer', chip_num=13)
