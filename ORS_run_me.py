import ashes_fg as af
from ashes_fg.examples import c4_offchip, cs_amp

af.fpaa.compile(cs_amp, project_name='cs_amp', chip_num=13)
