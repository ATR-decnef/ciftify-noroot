#!/usr/bin/env python3
import os
import unittest
import logging
import shutil
import tempfile
import ciftify.config
from ciftify.utils import run

from pytest import raises
from unittest.mock import patch

def get_test_data_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

test_dtseries = os.path.join(get_test_data_path(),
        'sub-50005_task-rest_Atlas_s0.dtseries.nii')
test_nifti = os.path.join(get_test_data_path(),
        'sub-50005_task-rest_bold_space-MNI152NLin2009cAsym_preproc.nii.gz')
left_surface = os.path.join(get_test_data_path(),
        'sub-50005.L.midthickness.32k_fs_LR.surf.gii')
right_surface = os.path.join(get_test_data_path(),
        'sub-50005.R.midthickness.32k_fs_LR.surf.gii')

class TestCitifySurfaceRois(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mkdtemp()
        vertices2_csv = os.path.join(src_data_dir, 'vertices1.csv')
        vertices1_csv = os.path.join(src_data_dir, 'vertices1.csv')

        with open(vertices1_csv, "w") as text_file:
            text_file.write('''hemi,vertex
        L,11801
        L,26245
        L,26235
        L,26257
        L,13356
        L,289
        L,13336
        L,13337
        L,26269
        L,13323
        L,26204
        '''
        # create a temp outputdir

    def tearDown(self):
        shutil.rmtree(self.path)


    def test_ciftify_surface_rois_gaussian(self):

        vertices1_csv = os.path.join(self.path, 'vertices1.csv')

        with open(vertices1_csv, "w") as text_file:
            text_file.write('''hemi,vertex
        L,11801
        L,26245
        L,26235
        L,26257
        L,13356
        L,289
        L,13336
        L,13337
        L,26269
        L,13323
        L,26204
        '''

        output_dscalar = os.path.join(self.path, 'gaussian.dscalar.nii')
        run(['ciftify_surface_rois', vertices1_csv, '10', '--gaussian',
             left_surface,
             right_surface,
             output_dscalar)])
        assert os.path.isfile(output_dscalar)


    def test_ciftify_surface_rois_probmap(self):

        vertices2_csv = os.path.join(self.path, 'vertices1.csv')
        with open(vertices2_csv, "w") as text_file:
            text_file.write('''hemi,vertex
        R,2379
        R,2423
        R,2423
        R,2629
        R,29290
        R,29290
        '''

        output_dscalar = os.path.join(self.path, 'probmap.dscalar.nii')
        run(['ciftify_surface_rois', vertices2_csv, '10', '--probmap',
             left_surface,
             right_surface,
             output_dscalar)])
        assert os.path.isfile(output_dscalar)

    def test_ciftify_surface_rois_with_labels(self):

        output_dscalar = os.path.join(self.path, 'pint_template.dscalar.nii')
        run(['ciftify_surface_rois',
              os.path.join(ciftify.config.find_ciftify_global(), 'PINT', 'Yeo7_2011_80verts.csv'),
              '6',
              '--vertex-col', 'tvertex',
              '--labels-col', 'NETWORK',
              '--overlap-logic', 'EXCLUDE',
              os.path.join(ciftify.config.find_HCP_S1200_GroupAvg(),
                        'S1200.L.midthickness_MSMAll.32k_fs_LR.surf.gii'),
              os.path.join(ciftify.config.find_HCP_S1200_GroupAvg(),
                        'S1200.R.midthickness_MSMAll.32k_fs_LR.surf.gii'),
              os.path.join(new_outputs, 'rois', 'tvertex.dscalar.nii')])
        assert os.path.isfile(output_dscalar)
                            
# ciftify_meants <nifti_func> <nifti_seed>
# ciftify_meants <cifti_func> <cifti_seed> (cifti_seed - subcortical)
  # results of a and b should match (as long as the nifti came from them cifti)
                            
# ciftify_meants <cifti_func> <cifti_seed> (cifti_seed - cortical)
# ciftify_meants <cifti_func> <gifti_seed> 
# ciftify_meants <gifti_func> <gifti_seed>
  # results of a, b, and c should match
                            
# ciftify_meants (weighted)
# ciftify_meants (with a label)
# ciftify_meants (with multiple entries) - dlabel (no labels)
# ciftify_meants (with multiple entries) - dlabel (w labels)
# ciftify_meants (with multiple entries) - dscalar (no labels)
# ciftify_meants (with multiple entries) - dscalar (w labels) 
# ciftify_meants (with mask)
                            
# ciftify_seedcorr with a TR drop                            
#   TR_file = os.path.join(new_outputs, 'rois','TR_file.txt')
# with open(TR_file, "w") as text_file:
#     text_file.write('''1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30''')                          
# ciftify_seedcorr with mask                            
# ciftify seedcorr with cifti_output
# ciftify_seedcorr with cifti out w mask
# ciftify_seedcorr with nifti_output
# ciftify_seedcorr with nifti_output w mask
# ciftify_seedcorr with with fisher-z
                          
