import argparse
import unittest

import product


class JustTest(unittest.TestCase):

    def test_correct_product_returned_arm(self):
        args = argparse.Namespace()
        args.product_number = "CXF1010100/2"
        args.product_version = "2.365.0"
        args.arm_url = "https://arm.sero.gic.ericsson.se/artifactory/proj-exilis-released-generic-local/eric-ran-du" \
                       "-nr/2.365.0/Cloud_RAN_DU-2.365.0-CXF1010100_2-R366A.zip "
        args.gerrit_url = None

        determine_product = product.determine_product(args)
        self.assertIn("arm", determine_product.values(), msg="Type didn't matched")
