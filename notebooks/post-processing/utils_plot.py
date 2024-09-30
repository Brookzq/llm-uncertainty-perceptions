import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os

from matplotlib.ticker import MultipleLocator, PercentFormatter


FULL_WIDTH, COL_WIDTH = 6.30045, 3.03209
DEF_SIZE = FULL_WIDTH, FULL_HEIGHT


# Accessibility
sns.set_palette(sns.color_palette("colorblind"))
matplotlib.rcParams["axes.prop_cycle"] = matplotlib.cycler(color=sns.color_palette("colorblind"))

matplotlib.rc('font', family='serif', size=12)
matplotlib.rc('text', usetex=True)


def adjust(fig, left=0.0, right=1.0, bottom=0.0, top=1.0, wspace=0.0, hspace=0.0):
    fig.subplots_adjust(
        left   = left,  # the left side of the subplots of the figure
        right  = right,  # the right side of the subplots of the figure
        bottom = bottom,  # the bottom of the subplots of the figure
        top    = top,  # the top of the subplots of the figure
        wspace = wspace,  # the amount of width reserved for blank space between subplots
        hspace = hspace,  # the amount of height reserved for white space between subplots
    )
    
def save_fig(fig, path, **kwargs):
    os.makedirs(path.rpartition("/")[0], exist_ok=True)
    path = path.replace(".json", "")
    print(path)
    fig.savefig(path, bbox_inches="tight", **kwargs)
