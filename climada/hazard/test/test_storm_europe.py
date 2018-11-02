"""
This file is part of CLIMADA.

Copyright (C) 2017 CLIMADA contributors listed in AUTHORS.

CLIMADA is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free
Software Foundation, version 3.

CLIMADA is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with CLIMADA. If not, see <https://www.gnu.org/licenses/>.

---

Test StormEurope class
"""

import os
import unittest
import datetime as dt
import numpy as np
from scipy import sparse

from climada.hazard import StormEurope, Centroids
from climada.util import GridPoints

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class TestReader(unittest.TestCase):
    """ Test loading functions from the StormEurope class """

    fn = [
        'fp_lothar_crop-test.nc',
        'fp_xynthia_crop-test.nc',
    ]
    ncdfs = [os.path.join(DATA_DIR, f) for f in fn]

    ct = Centroids(os.path.join(DATA_DIR, 'fp_centroids-test.csv'))

    def test_centroids_from_nc(self):
        """ Test if centroids can be constructed correctly """
        ct = StormEurope._centroids_from_nc(self.ncdfs[0])

        self.assertTrue(isinstance(ct, Centroids))
        self.assertTrue(isinstance(ct.coord, GridPoints))
        self.assertEqual(ct.size, 10000)
        self.assertEqual(ct.coord.shape[0], ct.id.shape[0])

    def test_read_footprints(self):
        """ Test read_footprints function, using two small test files"""
        se = StormEurope()
        se.read_footprints(self.ncdfs)

        self.assertEqual(se.tag.haz_type, 'WS')
        self.assertEqual(se.units, 'm/s')
        self.assertEqual(se.event_id.size, 2)
        self.assertEqual(se.date.size, 2)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).year, 1999)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).month, 12)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).day, 26)
        self.assertEqual(se.event_id[0], 1)
        self.assertEqual(se.event_name[0], 'Lothar')
        self.assertTrue(isinstance(se.intensity, sparse.csr.csr_matrix))
        self.assertTrue(isinstance(se.fraction, sparse.csr.csr_matrix))
        self.assertEqual(se.intensity.shape, (2, 10000))
        self.assertEqual(se.fraction.shape, (2, 10000))

    def test_read_with_ref(self):
        """ Test read_footprints while passing in a reference raster. """
        se = StormEurope()
        se.read_footprints(self.ncdfs, ref_raster=self.ncdfs[1])

        self.assertEqual(se.tag.haz_type, 'WS')
        self.assertEqual(se.units, 'm/s')
        self.assertEqual(se.event_id.size, 2)
        self.assertEqual(se.date.size, 2)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).year, 1999)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).month, 12)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).day, 26)
        self.assertEqual(se.event_id[0], 1)
        self.assertEqual(se.event_name[0], 'Lothar')
        self.assertTrue(isinstance(se.intensity, sparse.csr.csr_matrix))
        self.assertTrue(isinstance(se.fraction, sparse.csr.csr_matrix))
        self.assertEqual(se.intensity.shape, (2, 10000))
        self.assertEqual(se.fraction.shape, (2, 10000))

    def test_read_with_cent(self):
        """ Test read_footprints while passing in a Centroids object """
        se = StormEurope()
        se.read_footprints(self.ncdfs, centroids=self.ct)

        self.assertEqual(se.tag.haz_type, 'WS')
        self.assertEqual(se.units, 'm/s')
        self.assertEqual(se.event_id.size, 2)
        self.assertEqual(se.date.size, 2)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).year, 1999)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).month, 12)
        self.assertEqual(dt.datetime.fromordinal(se.date[0]).day, 26)
        self.assertEqual(se.event_id[0], 1)
        self.assertEqual(se.event_name[0], 'Lothar')
        self.assertTrue(isinstance(se.intensity, sparse.csr.csr_matrix))
        self.assertTrue(isinstance(se.fraction, sparse.csr.csr_matrix))
        self.assertEqual(se.intensity.shape, (2, 10000))
        self.assertEqual(se.fraction.shape, (2, 10000))
        self.assertEqual(
            se.centroids.region_id[
                np.isnan(se.centroids.region_id)
            ].size,
            7515
        )


# Execute Tests
TESTS = unittest.TestLoader().loadTestsFromTestCase(TestReader)
unittest.TextTestRunner(verbosity=2).run(TESTS)
