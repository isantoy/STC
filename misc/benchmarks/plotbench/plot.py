import sys
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
#sns.set_theme(style="whitegrid")

comp = ['All compilers', 'Mingw-g++-13.1.0', 'Win-Clang-16.0.5', 'VC-19.36']
n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
file = sys.argv[2] if len(sys.argv) > 2 else 'plot_win.csv'
df = pd.read_csv(file)
df = df[df.Method != 'total']
if n > 0:
    df = df[df.Compiler == comp[n]]

g = sns.catplot(data=df, x='Method', y='Seconds', hue='Library', col='C', kind='bar', orient='v',
                 errorbar=('ci', 68), legend=False, col_wrap=2, sharex=False, aspect=1.4, height=3.0)
g.set_xlabels('')

g.add_legend(bbox_to_anchor=(0.75, 0.2), borderaxespad=0)
g.fig.subplots_adjust(top=0.90, left=0.08, right=0.98, bottom=0.04, hspace=0.4)
g.fig.suptitle('Benchmark STC vs c++ std containers: %s' % comp[n], fontsize=15, y=0.98)

plt.show()
