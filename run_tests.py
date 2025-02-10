#!/usr/bin/env python3
"""
UI総合テスト実行スクリプト
Created: 2025-02-09 14:59:16
Author: GingaDza
"""

import unittest
import sys
import os

def run_tests():
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)