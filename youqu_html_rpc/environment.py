import collections
import functools
import getpass
import os


def wf(f, t):
    f.write(t.encode("unicode_escape").decode() + "\n")


def collect_result(execute):
    res = collections.Counter([execute.get(i).get("result") for i in execute])
    _total = sum(res.values())
    skiped = res.get("skip", 0)
    total = _total - skiped
    passed = res.get("pass", 0)
    failed = total - passed
    pass_rate = f"{round((passed / total) * 100, 2)}%" if passed else "0%"
    return total, failed, passed, skiped, pass_rate


def environment(data_path):
    if not data_path:
        return
    allure_fspath_path = os.path.join(data_path, "environment.properties")
    with open(allure_fspath_path, "w+", encoding="utf-8") as _f:
        w = functools.partial(wf, _f)

        w(f"""CPU信息={os.popen('cat /proc/cpuinfo | grep "model name"').read()}""")
        w(f"内存信息={os.popen('cat /proc/meminfo | grep MemTotal').read()}")

        w(f"USER={getpass.getuser()}")
        w(f"IP={os.popen('hostname -I').read()}")
        w(f"内核信息={os.popen('uname -a').read()}")
        w(f"分辨率={os.popen('xrandr').read()}")
