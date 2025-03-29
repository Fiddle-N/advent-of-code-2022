from day_07 import process


def test_process_terminal_out() -> None:
    out = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    dir_ = process.process_out(out)

    d = process.Dir(
        files={"j": 4060174, "d.log": 8033020, "d.ext": 5626152, "k": 7214296},
        parent=None,
    )

    e = process.Dir(
        files={
            "i": 584,
        },
        parent=None,
    )

    a = process.Dir(files={"e": e, "f": 29116, "g": 2557, "h.lst": 62596}, parent=None)

    e.parent = a

    root = process.Dir(
        files={"a": a, "b.txt": 14848514, "c.dat": 8504156, "d": d}, parent=None
    )

    a.parent = root
    d.parent = root

    assert dir_ == root


def test_dirs_below_100k() -> None:
    terminal_out = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    filesystem = process.process_out(terminal_out)

    assert isinstance(filesystem.files['a'], process.Dir)

    assert process.dirs_below_100k(filesystem) == [
        filesystem.files["a"],
        filesystem.files["a"].files["e"],
    ]


def test_sum_dirs_below_100k() -> None:
    terminal_out = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    filesystem = process.process_out(terminal_out)

    assert process.sum_dirs_below_100k(filesystem) == 95437


def test_dirs_to_free_space() -> None:
    terminal_out = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    filesystem = process.process_out(terminal_out)

    assert process.dirs_to_free_space(filesystem) == [filesystem, filesystem.files["d"]]


def test_min_dir_size_to_free_space() -> None:
    terminal_out = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
    filesystem = process.process_out(terminal_out)

    assert process.min_dir_size_to_free_space(filesystem) == 24933642
