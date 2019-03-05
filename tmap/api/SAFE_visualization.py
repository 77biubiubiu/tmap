import argparse
import os
import pickle
from collections import Counter

import numpy as np
import pandas as pd
import plotly
import plotly.io as pio
from plotly import graph_objs as go
from plotly import tools
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

from tmap.api.general import data_parser, logger


def draw_PCOA(rawdata, summary_data, output, mode='html', width=1500, height=1000, sort_col='SAFE enriched score'):
    fig = go.Figure()
    safe_df = pd.DataFrame.from_dict(rawdata)
    safe_df = safe_df.reindex(columns=summary_data.index)
    pca = PCA()
    pca_result = pca.fit_transform(safe_df.T)

    mx_scale = MinMaxScaler(feature_range=(10, 40)).fit(summary_data.loc[:, [sort_col]])

    vals = summary_data.loc[:, [sort_col]]
    fig.add_trace(go.Scatter(x=pca_result[:, 0],
                             y=pca_result[:, 1],
                             mode="markers",
                             marker=dict(  # color=color_codes[cat],
                                 size=mx_scale.transform(vals),
                                 opacity=0.5),
                             showlegend=False,
                             text=summary_data.index))

    fig.add_trace(go.Scatter(x=pca_result[:, 0],
                             y=pca_result[:, 1],
                             # visible=False,
                             mode="text",
                             hoverinfo='none',
                             textposition="middle center",
                             name='name for searching',
                             showlegend=False,
                             textfont=dict(size=13),
                             text=''))

    fig.layout.update(dict(xaxis=dict(title="PC1({:.2f}%)".format(pca.explained_variance_ratio_[0] * 100)),
                           yaxis=dict(title="PC2({:.2f}%)".format(pca.explained_variance_ratio_[1] * 100)),
                           width=width,
                           height=height,
                           font=dict(size=15),
                           hovermode='closest', ))
    if mode != 'html':
        pio.write_image(fig, output, format=mode)
    else:
        plotly.offline.plot(fig, filename=output, auto_open=False)


def draw_stratification(graph, SAFE_dict, output, mode='html', n_iter=1000, p_val=0.05, width=1000, height=1000):
    # Enterotyping-like stratification map based on SAFE score
    node_pos = graph["node_positions"]
    sizes = graph["node_sizes"][:, 0]
    xs = []
    ys = []
    for edge in graph["edges"]:
        xs += [node_pos[edge[0], 0],
               node_pos[edge[1], 0],
               None]
        ys += [node_pos[edge[0], 1],
               node_pos[edge[1], 1],
               None]
    fig = plotly.tools.make_subplots(1, 1)

    node_line = go.Scatter(
        # ordination line
        visible=True,
        x=xs,
        y=ys,
        marker=dict(color="#8E9DA2",
                    opacity=0.7),
        line=dict(width=1),
        showlegend=False,
        mode="lines")
    fig.append_trace(node_line, 1, 1)

    safe_score_df = pd.DataFrame.from_dict(SAFE_dict)
    min_p_value = 1.0 / (n_iter + 1.0)
    SAFE_pvalue = np.log10(p_val) / np.log10(min_p_value)
    tmp = [safe_score_df.columns[_] if safe_score_df.iloc[idx, _] > SAFE_pvalue else np.nan for idx, _ in enumerate(np.argmax(safe_score_df.values, axis=1))]
    t = Counter(tmp)
    for idx, fea in enumerate([_ for _, v in sorted(t.items(), key=lambda x: x[1]) if v >= 10]):
        # safe higher than threshold, just centroides
        node_position = go.Scatter(
            # node position
            visible=True,
            x=node_pos[np.array(tmp) == fea, 0],
            y=node_pos[np.array(tmp) == fea, 1],
            hoverinfo="text",
            marker=dict(  # color=node_colors,
                size=[5 + sizes[_] for _ in np.arange(node_pos.shape[0])[np.array(tmp) == fea]],
                opacity=0.9),
            showlegend=True,
            name=fea + ' (%s)' % str(t[fea]),
            mode="markers")
        fig.append_trace(node_position, 1, 1)
    fig.layout.width = width
    fig.layout.height = height
    fig.layout.font.size = 30
    fig.layout.hovermode = 'closest'

    if mode != 'html':
        pio.write_image(fig, output, format=mode)
    else:
        plotly.offline.plot(fig, filename=output, auto_open=False)


def process_summary_paths(safe_summaries):
    datas = [data_parser(path, verbose=0) for path in safe_summaries]
    if len(datas) > 1:
        if len(set.union(*[set(_.index) for _ in datas])) != datas[0].shape[0]:
            # if different index between datas
            logger("Different index found between multiple input SAFE summary files...", verbose=1)
            return
        else:
            cols_dict = {}
            for path, data in zip(safe_summaries, datas):
                name = os.path.basename(path).strip('.csv')
                data.columns = ['%s (%s)' % (col, name) for col in data.columns]
                cols_dict[name] = data.columns
            data = pd.concat(datas, axis=1)
    else:
        data = datas[0]
        cols_dict = {'Only one df': data.columns}
    return data, cols_dict


def draw_ranking(data, cols_dict, output, mode='html', width=1600, height=1400, sort_col='SAFE enriched score'):
    col_names = list(cols_dict.keys())
    if len(col_names) == 1:
        fig = tools.make_subplots(1, 1)
    else:
        fig = tools.make_subplots(1, len(cols_dict), shared_yaxes=True, horizontal_spacing=0, subplot_titles=col_names)

    sorted_df = data.sort_values([_ for _ in data.columns if _.startswith(sort_col)], ascending=False)

    def _add_trace(name, col):
        fig.append_trace(go.Bar(x=sorted_df.loc[:, name],
                                y=sorted_df.index,
                                marker=dict(
                                    line=dict(width=1)
                                ),
                                orientation='h',
                                showlegend=False),
                         1, col)

    for idx, each in enumerate(col_names):
        col = idx + 1
        name = [_ for _ in cols_dict[each] if _.startswith(sort_col)][0]
        _add_trace(name, col)

    fig.layout.yaxis.autorange = 'reversed'

    fig.layout.margin.l = width/4
    fig.layout.width = width
    fig.layout.height = height

    if mode != 'html':
        pio.write_image(fig, output, format=mode)
    else:
        plotly.offline.plot(fig, filename=output, auto_open=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mission", help="Which kinds of graph you want to generate. \
                         [ranking|stratification|ordination]",
                        type=str, choices=['ranking', 'stratification', 'ordination'])
    parser.add_argument("-G", "--graph", help="Graph file computed from 'Network_generator.py'.",
                        type=str)
    parser.add_argument("-O", "--output", help="Prefix of output file",
                        type=str)
    parser.add_argument("-S1", "--SAFE", help="Pickled dict contains raw SAFE scores.",
                        type=str)
    parser.add_argument("-S2", "--SAFE_summary", dest='sum_s', nargs='*', help="Summary of SAFE scores",
                        type=str)
    parser.add_argument("--sort", help="The column you need to sort with",
                        type=str, default='SAFE enriched score')
    parser.add_argument("-p", "--pvalue",
                        help="p-val for decide which level of data should consider as significant",
                        default=0.05, type=float)
    parser.add_argument("--type", help="The file type to output figure. [pdf|html|png]",
                        type=str, default='html')
    parser.add_argument("--width", help="The height of output picture",
                        type=int,default=1600)
    parser.add_argument("--height", help="The width of output picture",
                        type=int,default=1600)

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    if args.mission == 'ranking':
        data, cols_dict = process_summary_paths(args.sum_s)
        draw_ranking(data=data,
                     cols_dict=cols_dict,
                     output=args.output,
                     mode=args.type,
                     height=args.height,
                     width=args.width,
                     sort_col=args.sort)
    elif args.mission == 'stratification':
        dict_data = pickle.load(open(args.SAFE, 'rb'))
        safe_dict = dict_data['data']
        n_iter = dict_data['params']['n_iter']
        graph = pickle.load(open(args.graph, 'rb'))
        draw_stratification(graph=graph,
                            SAFE_dict=safe_dict,
                            output=args.output,
                            mode=args.type,
                            n_iter=n_iter,
                            p_val=args.pvalue,
                            width=args.width,
                            height=args.height)
    elif args.mission == 'ordination':
        dict_data = pickle.load(open(args.SAFE, 'rb'))
        safe_dict = dict_data['data']
        data, cols_dict = process_summary_paths(args.sum_s)
        graph = pickle.load(open(args.graph, 'rb'))
        col_names = list(cols_dict.keys())
        if len(col_names) != 1:
            logger("The number of raw data of SAFE needs to match the number of summary input.", verbose=1)
        else:
            draw_PCOA(rawdata=safe_dict,
                      summary_data=data,
                      output=args.output,
                      mode=args.type,
                      height=args.height,
                      width=args.width,
                      sort_col=args.sort)