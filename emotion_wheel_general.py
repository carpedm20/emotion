from __future__ import annotations

from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import math
import re

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import to_rgb
from matplotlib.patches import Wedge


@dataclass
class Node:
    name: str
    children: List["Node"] = field(default_factory=list)
    leaf_count: int = 0
    depth: int = 0
    parent: Optional["Node"] = None
    branch_color: Optional[Tuple[float, float, float]] = None


DEFAULT_ANCHOR_PALETTE = [
    "#e58f93",  # negative / high-ish
    "#9bb7d7",  # negative / low-ish
    "#ead78b",  # positive / high-ish
    "#9fcca9",  # positive / low-ish
    "#c6abd6",
    "#a7d6d1",
    "#efc08f",
    "#c7d88a",
]


def _is_scalar_leaf(x: Any) -> bool:
    return isinstance(x, (str, int, float, bool)) or x is None


def _parse_node(name: str, obj: Any, *, parent: Optional[Node] = None, depth: int = 0) -> Node:
    """
    Supported inputs:
      - nested dicts
      - lists/tuples of scalar leaves
      - lists of singleton dicts
      - lists of {"name": ..., "children": ...}
    """
    node = Node(str(name), parent=parent, depth=depth)

    if isinstance(obj, dict):
        for k, v in obj.items():
            node.children.append(_parse_node(k, v, parent=node, depth=depth + 1))
        return node

    if isinstance(obj, (list, tuple)):
        if all(_is_scalar_leaf(v) for v in obj):
            for v in obj:
                node.children.append(_parse_node(str(v), [], parent=node, depth=depth + 1))
            return node

        for i, item in enumerate(obj):
            if isinstance(item, dict):
                if set(item.keys()) >= {"name", "children"}:
                    node.children.append(
                        _parse_node(str(item["name"]), item["children"], parent=node, depth=depth + 1)
                    )
                elif len(item) == 1:
                    k, v = next(iter(item.items()))
                    node.children.append(_parse_node(str(k), v, parent=node, depth=depth + 1))
                else:
                    node.children.append(_parse_node(f"Item {i + 1}", item, parent=node, depth=depth + 1))
            else:
                node.children.append(_parse_node(str(item), [], parent=node, depth=depth + 1))
        return node

    # Scalar terminal.
    return node


def _compute_leaf_counts(node: Node) -> int:
    if not node.children:
        node.leaf_count = 1
    else:
        node.leaf_count = sum(_compute_leaf_counts(c) for c in node.children)
    return node.leaf_count


def _tree_depth(node: Node) -> int:
    if not node.children:
        return 0
    return 1 + max(_tree_depth(c) for c in node.children)


def _nodes_by_depth(node: Node) -> Dict[int, List[Node]]:
    levels: Dict[int, List[Node]] = defaultdict(list)
    stack = [node]
    while stack:
        n = stack.pop()
        levels[n.depth].append(n)
        stack.extend(reversed(n.children))
    return levels


def _contains_korean(text: str) -> bool:
    return any("\uac00" <= ch <= "\ud7a3" for ch in text)


def _choose_font() -> str:
    """
    Pick a font that supports Hangul if available.
    """
    candidates = [
        "AppleGothic",
        "NanumGothic",
        "Noto Sans CJK KR",
        "Malgun Gothic",
        "DejaVu Sans",
    ]

    installed = {f.name for f in fm.fontManager.ttflist}

    for candidate in candidates:
        if candidate in installed:
            return candidate

    return "DejaVu Sans"


def display_label(label: str, *, title_case: bool = True, strip_meta_suffixes: bool = True) -> str:
    """
    Human readable label formatter.

    Works for:
    - English keys
    - Korean keys
    - mixed Korean + English
    """
    s = str(label).replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()

    # Remove meta suffixes only for English tokens.
    if strip_meta_suffixes and not _contains_korean(s):
        for suffix in [" VALENCE", " AROUSAL", " CONTEXT", " FAMILY"]:
            if s.upper().endswith(suffix):
                s = s[: -len(suffix)]
                break

    if _contains_korean(s):
        # Korean should never be title-cased.
        return s

    if not title_case:
        return s

    small_words = {"of", "and", "or", "the", "a", "an", "in", "on", "to", "for", "vs"}
    out: List[str] = []
    for i, w in enumerate(s.split()):
        if i > 0 and w.lower() in small_words:
            out.append(w.lower())
        else:
            out.append(w.capitalize())
    return " ".join(out)


def _blend(c1: Any, c2: Any, t: float) -> Tuple[float, float, float]:
    r1, g1, b1 = to_rgb(c1)
    r2, g2, b2 = to_rgb(c2)
    return (
        r1 * (1 - t) + r2 * t,
        g1 * (1 - t) + g2 * t,
        b1 * (1 - t) + b2 * t,
    )


def _blend_many(colors: Sequence[Any]) -> Tuple[float, float, float]:
    cols = [to_rgb(c) for c in colors]
    n = len(cols)
    return tuple(sum(c[i] for c in cols) / n for i in range(3))  # type: ignore[return-value]


def _lighten(color: Any, amount: float) -> Tuple[float, float, float]:
    return _blend(color, (1, 1, 1), amount)


def _semantic_top_color(label: str) -> Optional[Tuple[float, float, float]]:
    u = str(label).upper()
    if "NEGATIVE" in u:
        return to_rgb("#d9d4d9")
    if "POSITIVE" in u:
        return to_rgb("#d9d4b8")
    return None


def _determine_anchor_depth(root: Node) -> int:
    """
    Pick the first non-leaf depth that is structurally informative enough
    to deserve its own color family.

    Examples
    --------
    Positive / Negative / High / Low / Family / Word
    -> color the High / Low ring, not the leaf ring.

    Generic tree with only 2 or 3 top-level groups
    -> fall back to the first visible level unless a better intermediate
       grouping exists.
    """
    levels = _nodes_by_depth(root)
    ring_count = _tree_depth(root)

    # Exclude the outer leaf ring from color anchoring.
    for depth in range(1, ring_count):
        count = len(levels.get(depth, []))
        if 4 <= count <= 12:
            return depth

    return 1


def _assign_branch_colors(root: Node, palette: Sequence[str]) -> int:
    levels = _nodes_by_depth(root)
    anchor_depth = _determine_anchor_depth(root)
    anchor_nodes = levels.get(anchor_depth, [])

    for i, node in enumerate(anchor_nodes):
        node.branch_color = to_rgb(palette[i % len(palette)])

    def nearest_anchor_ancestor(node: Node) -> Optional[Node]:
        cur: Optional[Node] = node
        while cur is not None and cur.depth > anchor_depth:
            cur = cur.parent
        if cur is not None and cur.depth == anchor_depth:
            return cur
        return None

    all_nodes: List[Node] = []
    stack = [root]
    while stack:
        n = stack.pop()
        all_nodes.append(n)
        stack.extend(n.children)

    for node in sorted(all_nodes, key=lambda n: -n.depth):
        if node.depth == 0:
            continue

        if node.depth >= anchor_depth:
            anc = node if node.depth == anchor_depth else nearest_anchor_ancestor(node)
            if anc is not None and anc.branch_color is not None:
                node.branch_color = anc.branch_color
            else:
                node.branch_color = to_rgb("#dddddd")
            continue

        semantic = _semantic_top_color(node.name)
        if semantic is not None:
            node.branch_color = semantic
            continue

        child_colors = [c.branch_color for c in node.children if c.branch_color is not None]
        if child_colors:
            node.branch_color = _blend_many(child_colors)
        else:
            node.branch_color = to_rgb("#dddddd")

    return anchor_depth


def _collect_label_stats(root: Node) -> Dict[int, Dict[str, float]]:
    levels = _nodes_by_depth(root)
    stats: Dict[int, Dict[str, float]] = {}
    for depth, nodes in levels.items():
        if depth == 0:
            continue
        labels = [display_label(n.name) for n in nodes]
        lengths = sorted(len(s) for s in labels)
        p90 = lengths[max(0, int(0.9 * len(lengths)) - 1)]
        stats[depth] = {
            "count": float(len(nodes)),
            "max_len": float(max(lengths)),
            "p90_len": float(p90),
            "avg_len": float(sum(lengths) / len(lengths)),
        }
    return stats


def _compute_ring_geometry(root: Node, *, max_radius: float = 1.0) -> Tuple[List[float], List[float]]:
    """
    Wider outer bands, because radial text uses band thickness as its main readable length.
    """
    ring_count = _tree_depth(root)
    stats = _collect_label_stats(root)

    weights: List[float] = []
    for level in range(1, ring_count + 1):
        p90 = stats[level]["p90_len"]
        weight = 1.0 + 0.035 * min(p90, 28) + 0.08 * (level - 1)
        if level == ring_count:
            weight += 0.45
        weights.append(weight)

    total = sum(weights)
    widths = [max_radius * w / total for w in weights]

    radii = [0.0]
    for w in widths:
        radii.append(radii[-1] + w)

    return widths, radii


def _polar_to_cart(r: float, theta_deg: float) -> Tuple[float, float]:
    t = math.radians(theta_deg)
    return r * math.cos(t), r * math.sin(t)


def _radial_rotation(theta_deg: float) -> float:
    rot = theta_deg % 360
    if 90 < rot < 270:
        rot += 180
    rot %= 360
    if 90 < rot < 270:
        rot -= 180
    return rot


def _estimate_fontsize(
    label: str,
    *,
    band_width: float,
    arc_span_deg: float,
    radius_mid: float,
    px_per_unit: float,
    ring_idx: int,
    ring_count: int,
) -> float:
    """
    Radial label logic:
    - main readable length ~= band thickness
    - cross direction ~= arc width at the label radius
    """
    char_count = max(2, len(label.replace("\n", "")))
    band_px = band_width * px_per_unit
    arc_px = math.radians(max(arc_span_deg, 0.1)) * max(radius_mid, band_width * 0.7) * px_per_unit

    fs_main = (band_px * 0.82) / (0.62 * char_count)
    fs_cross = (arc_px * 0.78) / 1.7
    fs = min(fs_main, fs_cross)

    fs *= 0.92 * (1.03 - 0.04 * (ring_idx / max(1, ring_count - 1)))
    return max(4.0, min(16.0, fs))


def _maybe_wrap_label(label: str, *, band_width: float, px_per_unit: float, target_fs: float) -> str:
    text = display_label(label)

    # Never wrap Korean text automatically.
    if _contains_korean(text):
        return text

    if " " not in text:
        return text

    band_px = band_width * px_per_unit
    approx_len_px = 0.62 * len(text) * target_fs
    if approx_len_px < band_px * 0.95:
        return text

    parts = text.split()
    best: Optional[Tuple[int, str]] = None
    for i in range(1, len(parts)):
        a = " ".join(parts[:i])
        b = " ".join(parts[i:])
        score = abs(len(a) - len(b))
        candidate = a + "\n" + b
        if best is None or score < best[0]:
            best = (score, candidate)
    return best[1] if best is not None else text


def _shade_for_ring(base_color: Any, ring_idx: int, ring_count: int) -> Tuple[float, float, float]:
    """
    Alternating soft / lighter / richer shades, similar to classic emotion wheel styling.
    """
    if ring_count == 1:
        amount = 0.15
    else:
        if ring_idx == 0:
            amount = 0.08
        elif ring_idx % 2 == 1:
            amount = 0.38
        else:
            amount = 0.20

        if ring_idx == ring_count - 1:
            amount = max(0.14, amount - 0.08)

    return _lighten(base_color, amount)


def draw_emotion_wheel(
    emotion_space: Any,
    *,
    title: Optional[str] = None,
    output_path: Optional[str] = None,
    palette: Sequence[str] = DEFAULT_ANCHOR_PALETTE,
    figure_inches: Optional[float] = None,
    dpi: int = 240,
    background: Optional[str] = None,
    transparent_background: Optional[bool] = None,
    show: bool = False,
) -> Dict[str, Any]:
    """
    Draw a clean, readable radial emotion wheel from any nested dict/list hierarchy.

    Parameters
    ----------
    emotion_space:
        Nested dict / list hierarchy.
    title:
        Optional title.
    output_path:
        File path to save PNG / SVG / PDF.
    palette:
        Branch anchor palette.
    figure_inches:
        Auto-sized if None.
    dpi:
        Raster resolution.
    background:
        Figure / axes background when transparency is disabled.
    transparent_background:
        Save with a transparent background. Defaults to True when no
        background is provided, otherwise False.
    show:
        Whether to call plt.show().

    Returns
    -------
    Dict[str, Any]
        Metadata for the rendered wheel.
    """
    root = _parse_node("ROOT", emotion_space)
    _compute_leaf_counts(root)
    ring_count = _tree_depth(root)
    anchor_depth = _assign_branch_colors(root, palette)
    ring_widths, radii = _compute_ring_geometry(root)
    leaf_count = root.leaf_count
    angle_per_leaf = 360.0 / leaf_count

    if figure_inches is None:
        figure_inches = min(24, max(16, 12 + leaf_count / 12 + ring_count * 1.5))

    if transparent_background is None:
        transparent_background = background is None

    resolved_background = "none" if transparent_background else (background or "#f3f3f3")

    fig, ax = plt.subplots(figsize=(figure_inches, figure_inches), dpi=dpi)
    fig.patch.set_facecolor(resolved_background)
    ax.set_facecolor(resolved_background)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.02, 1.02)
    ax.set_ylim(-1.02, 1.02)

    line_width = 1.0 if figure_inches < 20 else 1.2

    fig.canvas.draw()
    px_per_unit = ax.bbox.width / (ax.get_xlim()[1] - ax.get_xlim()[0])
    font_family = _choose_font()

    text_items: List[Tuple[Any, float, float, float, int, int]] = []

    def recurse(node: Node, start_angle: float) -> None:
        span = node.leaf_count * angle_per_leaf
        end_angle = start_angle + span

        if node.depth > 0:
            ring_idx = node.depth - 1
            r0 = radii[ring_idx]
            r1 = radii[ring_idx + 1]
            fill = _shade_for_ring(node.branch_color, ring_idx, ring_count)

            wedge = Wedge(
                (0, 0),
                r1,
                start_angle,
                end_angle,
                width=(r1 - r0),
                facecolor=fill,
                edgecolor="black",
                linewidth=line_width,
            )
            ax.add_patch(wedge)

            raw_label = display_label(node.name)
            theta = (start_angle + end_angle) / 2.0
            radius_mid = (r0 + r1) / 2.0
            fontsize = _estimate_fontsize(
                raw_label,
                band_width=(r1 - r0),
                arc_span_deg=span,
                radius_mid=radius_mid,
                px_per_unit=px_per_unit,
                ring_idx=ring_idx,
                ring_count=ring_count,
            )
            final_label = _maybe_wrap_label(node.name, band_width=(r1 - r0), px_per_unit=px_per_unit, target_fs=fontsize)

            x, y = _polar_to_cart(radius_mid, theta)
            txt = ax.text(
                x,
                y,
                final_label,
                ha="center",
                va="center",
                rotation=_radial_rotation(theta),
                rotation_mode="anchor",
                fontsize=fontsize,
                family=font_family,
                linespacing=0.90,
            )
            text_items.append((txt, r1 - r0, span, radius_mid, ring_idx, ring_count))

        cur = start_angle
        for child in node.children:
            recurse(child, cur)
            cur += child.leaf_count * angle_per_leaf

    current_angle = 90.0
    for child in root.children:
        recurse(child, current_angle)
        current_angle += child.leaf_count * angle_per_leaf

    fig.canvas.draw()

    for r in radii[1:]:
        ax.add_patch(plt.Circle((0, 0), r, fill=False, edgecolor="black", linewidth=line_width))

    if title:
        ax.text(0, 1.085, title, ha="center", va="bottom", fontsize=18, family=font_family)

    if output_path:
        savefig_kwargs = {
            "bbox_inches": "tight",
            "pad_inches": 0.06,
            "transparent": transparent_background,
        }
        if not transparent_background:
            savefig_kwargs["facecolor"] = fig.get_facecolor()
        fig.savefig(output_path, **savefig_kwargs)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return {
        "leaf_count": leaf_count,
        "ring_count": ring_count,
        "anchor_depth": anchor_depth,
        "figure_inches": figure_inches,
        "angle_per_leaf": angle_per_leaf,
        "output_path": output_path,
    }


def validate_emotion_space(emotion_space: Any) -> Dict[str, Any]:
    """
    Cheap structural validation, useful before drawing.
    """
    root = _parse_node("ROOT", emotion_space)
    leaf_count = _compute_leaf_counts(root)
    ring_count = _tree_depth(root)
    levels = _nodes_by_depth(root)

    assert leaf_count > 0, "Emotion space must contain at least one leaf."
    assert ring_count >= 1, "Emotion space must have at least one visible ring."

    visible_node_count = sum(len(v) for k, v in levels.items() if k > 0)
    return {
        "leaf_count": leaf_count,
        "ring_count": ring_count,
        "visible_node_count": visible_node_count,
        "depth_counts": {k: len(v) for k, v in levels.items() if k > 0},
    }
