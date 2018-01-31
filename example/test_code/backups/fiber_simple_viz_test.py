import nibabel as nib

from pyfat.io.load import load_tck
from pyfat.algorithm.fiber_simple_viz import fiber_simple_3d_show

tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100408/result/result20vs45/cc_20fib_only_node.tck'

imgtck = load_tck(tck_path)
streamlines = imgtck.streamlines

# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)
fiber_simple_3d_show(img, streamlines)
