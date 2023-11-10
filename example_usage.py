import ashes_fg as af
from ashes_fg.examples import vec_alice, the_small_asic_v2

af.fpaa.compile(vec_alice, project_name='vec_alice')
af.asic.compile(the_small_asic_v2, project_name='asic_alice')
