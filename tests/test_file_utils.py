from src.file_utils import read_lines_lazy


def test_reads_all_lines(tmp_path):
    path = tmp_path / "f.txt"
    path.write_text("a\nb\nc\n")
    lines = list(read_lines_lazy(str(path)))
    assert lines == ["a", "b", "c"]


def test_is_lazy(tmp_path):
    path = tmp_path / "f.txt"
    path.write_text("a\nb\nc\n")
    gen = read_lines_lazy(str(path))
    assert not isinstance(gen, list)
    assert next(gen) == "a"