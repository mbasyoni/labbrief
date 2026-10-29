"""The standalone benchmark must work in a clean checkout with no evidence dir."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class BenchmarkCLITests(unittest.TestCase):
    def test_clean_checkout_creates_report_directory(self):
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory(prefix='labbrief-benchmark-clean-') as folder:
            checkout = Path(folder)
            for name in ('benchmark_local_ml.py', 'local_ml.py'):
                shutil.copyfile(source / name, checkout / name)
            shutil.copytree(source / 'model_data', checkout / 'model_data')
            self.assertFalse((checkout / 'evidence').exists())

            result = subprocess.run(
                [sys.executable, 'benchmark_local_ml.py'], cwd=checkout,
                capture_output=True, text=True, timeout=45,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report_path = checkout / 'evidence' / 'local-ml-benchmark.json'
            self.assertTrue(report_path.is_file())
            report = json.loads(report_path.read_text())
            self.assertEqual(report['training_count'], 36)
            self.assertEqual(len(report['results']), report['heldout_count'])
            self.assertEqual(len(report['out_of_domain']), report['ood_count'])
            self.assertEqual(
                report['data_sha256']['train.json'],
                hashlib.sha256((checkout / 'model_data' / 'train.json').read_bytes()).hexdigest(),
            )
            self.assertIn('training_count', result.stdout)


if __name__ == '__main__':
    unittest.main()
