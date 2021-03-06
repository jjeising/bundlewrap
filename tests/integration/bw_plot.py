from os.path import join

from bundlewrap.utils.testing import make_repo, run


def test_groups_for_node(tmpdir):
    make_repo(
        tmpdir,
        nodes={
            "node-foo": {},
            "node-bar": {},
            "node-baz": {},
            "node-pop": {},
        },
    )
    with open(join(str(tmpdir), "groups.py"), 'w') as f:
        f.write("""
groups = {
    "group-foo": {
        'members': ["node-foo"],
        'member_patterns': [r".*-bar"],
    },
    "group-bar": {
        'subgroups': ["group-foo"],
    },
    "group-baz": {
        'members': ["node-pop"],
        'members_add': lambda node: node.name == "node-pop",
    },
    "group-pop": {
        'subgroup_patterns': [r"ba"],
    },
}
    """)
    stdout, stderr, rcode = run("bw plot groups-for-node node-foo", path=str(tmpdir))
    assert stdout == b"""digraph bundlewrap
{
rankdir = LR
node [color="#303030"; fillcolor="#303030"; fontname=Helvetica]
edge [arrowhead=vee]
"group-bar" [fontcolor=white,style=filled];
"group-foo" [fontcolor=white,style=filled];
"group-pop" [fontcolor=white,style=filled];
"node-foo" [fontcolor="#303030",shape=box,style=rounded];
"group-bar" -> "group-foo" [color="#6BB753",penwidth=2]
"group-pop" -> "group-bar" [color="#6BB753",penwidth=2]
"group-foo" -> "node-foo" [color="#D18C57",penwidth=2]
}
"""
    assert stderr == b""
    assert rcode == 0

    stdout, stderr, rcode = run("bw plot groups-for-node node-pop", path=str(tmpdir))
    assert stdout == b"""digraph bundlewrap
{
rankdir = LR
node [color="#303030"; fillcolor="#303030"; fontname=Helvetica]
edge [arrowhead=vee]
"group-baz" [fontcolor=white,style=filled];
"group-pop" [fontcolor=white,style=filled];
"node-pop" [fontcolor="#303030",shape=box,style=rounded];
"group-pop" -> "group-baz" [color="#6BB753",penwidth=2]
"group-baz" -> "node-pop" [color="#D18C57",penwidth=2]
}
"""
    assert stderr == b""
    assert rcode == 0
