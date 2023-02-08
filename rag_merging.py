from skimage import data, segmentation, color
from skimage.future import graph
import numpy as np
import cv2

# 1. Using Superpixel to segment images
# 2. Create region adjacency graph
# 3. Merge adjacent regions base on certain thershold


def _weight_mean_color(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the `"weight"` attribute set as the absolute
        difference of the mean color between node `dst` and `n`.
    """

    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                      graph.nodes[dst]['pixel count'])



def super_pixel(img_path, p1, p2, p3, p4, p5):
        img = data.coffee()
        img = cv2.imread(img_path)
        img = img[:, :, [2, 1, 0]]


        labels = segmentation.slic(img, compactness=p1, n_segments=p2, start_label=p3, sigma=p4)
        g = graph.rag_mean_color(img, labels)

        labels2 = graph.merge_hierarchical(labels, g, thresh=p5, rag_copy=False,
                                        in_place_merge=True,
                                        merge_func=merge_mean_color,
                                        weight_func=_weight_mean_color)


        out = color.label2rgb(labels2, img, kind='avg', bg_label=0)
                
        return out  

