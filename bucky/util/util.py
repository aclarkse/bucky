"""Generic utility functions/classes used in the model."""

# TODO break into files now that we have the utils submodule (also update __init__)

import copy
import logging

import numpy as np
import pandas as pd
import tqdm


class TqdmLoggingHandler(logging.Handler):
    """Logging handler that is friendly with tqdm.

    See https://stackoverflow.com/questions/38543506/change-logging-print-function-to-tqdm-write-so-logging-doesnt-interfere-wit
    """

    def __init__(self, level=logging.NOTSET):  # pylint: disable=useless-super-delegation
        """Init handler."""
        super().__init__(level)

    def emit(self, record):
        """Emit message."""

        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):  # pylint: disable=try-except-raise
            raise
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)


class dotdict(dict):
    """dot.notation access to dictionary attributes."""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __deepcopy__(self, memo=None):
        """Return a deepcopy of the dict."""
        return dotdict({key: copy.deepcopy(value) for key, value in self.items()})


def remove_chars(seq):
    """Remove all non digit characters from a string, but cleanly passthrough non strs.

    Parameters
    ----------
    seq : any type
        Strings will be modified, any other type is directly returned

    Returns
    -------
    same type as seq
        The original sequence, minus non-digit characters if input was a string

    """
    seq_type = type(seq)
    if seq_type != str:
        return seq

    return seq_type().join(filter(seq_type.isdigit, seq))


def map_np_array(a, d):
    """Function similar to pandas map but for np arrays.

    .. deprecated:: 0.8.0
    """
    n = np.ndarray(a.shape)
    for k in d:
        n[a == k] = d[k]
    return n


def estimate_IFR(age):
    """Estimate the best fit IFR for a given age.

    See https://www.medrxiv.org/content/10.1101/2020.07.23.20160895v4.full.pdf for the fit

    Parameters
    ----------
    age : ndarray
        Array of ages to calculate IFR for

    Returns
    -------
    ifr : ndarray
        The calculated best fit IFR
    """

    # std err is 0.17 on the const and 0.003 on the linear term

    ifr = np.exp(-7.56 + 0.121 * age) / 100.0
    return ifr


def bin_age_csv(filename, out_filename):
    """Group ages in the Census csv to match the bins used by Prem et al.

    Parameters
    ----------
    filename : str
        Location of Census CSV
    out_filename : str
        Output filename for binned data

    """
    df = pd.read_csv(filename, header=None, names=["fips", "age", "N"])
    pop_weighted_IFR = df.N.to_numpy() * estimate_IFR(df.age.to_numpy())
    df = df.assign(IFR=pop_weighted_IFR)
    df["age_group"] = pd.cut(df["age"], np.append(np.arange(0, 76, 5), 120), right=False)
    df = df.groupby(["fips", "age_group"]).sum()[["N", "IFR"]].unstack("age_group")

    df = df.assign(IFR=df.IFR / df.N)

    df.to_csv(out_filename)


def date_to_t_int(dates, start_date):
    """Find the indices of a list of dates internally used by time indexed arrays in the modeli."""
    # TODO handle varied dt
    return np.array([(date - start_date).days for date in dates], dtype=int)


def _banner():
    """A banner for the CLI."""
    print(r" ____             _          ")  # noqa: T001
    print(r"| __ ) _   _  ___| | ___   _ ")  # noqa: T001
    print(r"|  _ \| | | |/ __| |/ / | | |")  # noqa: T001
    print(r"| |_) | |_| | (__|   <| |_| |")  # noqa: T001
    print(r"|____/ \__,_|\___|_|\_\\__, |")  # noqa: T001
    print(r"                       |___/ ")  # noqa: T001
    print(r"                             ")  # noqa: T001
