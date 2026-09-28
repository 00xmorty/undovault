import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'undovault'


class UndoVaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.vim = self.root / 'vim'
        self.nvim = self.root / 'nvim'
        self.vim.mkdir()
        self.nvim.mkdir()
        (self.vim / 'secret').write_text('private', encoding='utf-8')

    def run_cli(self, *extra, nvim=None):
        return subprocess.run([sys.executable, str(SCRIPT), '--vim-dir', str(self.vim), '--nvim-dir', str(nvim or self.nvim), *map(str, extra)], capture_output=True, text=True)

    def test_read_only_no_names(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('1 regular files, 7 bytes', result.stdout)
        self.assertNotIn('secret', result.stdout)
        self.assertFalse((self.root / 'archive').exists())

    def test_archive_copy_and_refuse_overwrite(self):
        target = self.root / 'archive'
        result = self.run_cli('--archive-to', target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((target / 'vim' / 'secret').read_text(), 'private')
        self.assertEqual((self.vim / 'secret').read_text(), 'private')
        self.assertNotEqual(self.run_cli('--archive-to', target).returncode, 0)

    def test_shared_and_symlinks(self):
        (self.vim / 'link').symlink_to(self.vim / 'secret')
        result = self.run_cli(nvim=self.vim)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Shared directory: YES', result.stdout)
        self.assertIn('1 regular files', result.stdout)
        archive = self.root / 'shared-archive'
        self.assertEqual(self.run_cli('--archive-to', archive, nvim=self.vim).returncode, 0)
        self.assertFalse((archive / 'vim' / 'link').exists())

    def test_refuse_archive_inside_source(self):
        self.assertNotEqual(self.run_cli('--archive-to', self.vim / 'archive').returncode, 0)

    def test_refuse_symlink_root(self):
        link = self.root / 'linked'
        link.symlink_to(self.vim, target_is_directory=True)
        self.assertNotEqual(self.run_cli(nvim=link).returncode, 0)


if __name__ == '__main__':
    unittest.main()
