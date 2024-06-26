import argparse
import resource
import sys
from pathlib import Path

from torch.utils.data import DataLoader

# do not do this.
# resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 9223372036854775807))

root_dir: str = "../../"
ROOT_DIR = Path(root_dir).resolve()
sys.path.insert(0, str(ROOT_DIR))


from src.utils.dataset import LunaDataset
from src.utils.logconf import logging
from src.utils.util import enumerateWithEstimate

log = logging.getLogger(__name__)
# log.setLevel(logging.WARN)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)


class LunaPrepCacheApp:
    @classmethod
    def __init__(self, sys_argv=None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--batch-size",
            help="Batch size to use for training",
            default=1024,
            type=int,
        )
        parser.add_argument(
            "--num-workers",
            help="Number of worker processes for background data loading",
            default=8,
            type=int,
        )

        self.cli_args = parser.parse_args(sys_argv)

    def main(self):
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        self.prep_dl = DataLoader(
            LunaDataset(
                sortby_str="series_uid",
            ),
            batch_size=self.cli_args.batch_size,
            num_workers=self.cli_args.num_workers,
        )

        batch_iter = enumerateWithEstimate(
            self.prep_dl,
            "Stuffing cache",
            start_ndx=self.prep_dl.num_workers,
        )
        for _ in batch_iter:
            pass


if __name__ == "__main__":
    LunaPrepCacheApp().main()

# %%
