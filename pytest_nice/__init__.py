"""
"""

import pytest
import os

pep8 = None


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if os.path.exists(".pep8rc"):
        os.remove(".pep8rc")


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    global pep8
    cov = config.pluginmanager.getplugin("pytest_cov")
    if cov:
        directory = ""
        content = False
        if os.path.exists("setup.cfg"):
            file = open("setup.cfg", "r")
            lines = file.read()
            for line in lines.splitlines():
                if "[coverage:html]" in line:
                    content = True
                if content and "[" not in line:
                    if "directory" in line:
                        directory = line.split("=", 1)[1].strip()
        if os.path.exists(".coveragerc"):
            file = open(".coveragerc", "r")
            lines = file.read()
            for line in lines.splitlines():
                if "[html]" in line:
                    content = True
                if content and "[" not in line:
                    if "directory" in line:
                        directory = line.split("=", 1)[1].strip()

    if pep8:
        pep8.close()
        if directory:
            pep8 = open(".pep8rc")
            name = pep8.readline().strip()
            items = {}
            total_fails = 0
            while name:
                fails = {}
                pep8fail = pep8.readline().strip()
                keys = []
                while ":" in pep8fail:
                    keys.append(pep8fail.split(":", 1)[0])
                    fails[pep8fail.split(":", 1)[0]] = pep8fail.split(":", 1)[1].strip()
                    pep8fail = pep8.readline().strip()
                items[name] = len(fails)
                total_fails += len(fails)
                file = "{}{}{}.html".format(directory, os.sep, name.replace(os.sep, "_").replace(".py", "_py"))
                if os.path.exists(file):
                    content = open(file, "r")
                    lines = content.read().splitlines()
                    content.close()
                    content = open(file, "w")
                    pos = 0
                    for index, line in enumerate(lines):
                        if "exc shortkey_x button_toggle_exc" in line:
                            content.write(line)
                            content.write("\n")
                            if "PEP8" not in lines[index + 1]:
                                content.write("\t\t\t<span style='color:orange;background:gray'>{} PEP8</span>".format(len(fails)))
                                content.write("\n")
                        elif fails != {}:
                            if "t{}".format(keys[pos]) in line:
                                if "<span style='color:orange;background:gray'>" not in line:
                                    content.write("{}<span style='color:orange;background:gray'>{}</span>".format(line[:-4], fails[keys[pos]]))
                                    content.write("</p>\n")
                                else:
                                    content.write(line)
                                    content.write("\n")
                                del fails[keys[pos]]
                                pos += 1
                            else:
                                content.write(line)
                                content.write("\n")
                        else:
                            content.write(line)
                            content.write("\n")
                    content.close()
                name = pep8fail
            index = open(directory +  os.sep + "index.html", "r")
            index_lines = index.readlines()
            index.close()
            index = open(directory + os.sep + "/index.html", "w")
            header = False
            found_entry = False
            row = ""
            for line in index_lines:

                if header:
                    if "name" in line:
                        header = False
                        if "<a" in line:
                            row = line[:-10]
                        else:
                            row = line[:-6]
                        row = row.rsplit(">", 1)[1]
                if "PEP8" in line:
                    found_entry = True
                    if "Module" not in row:
                        if "Total" in row:
                            line = "\t\t\t\t<td>{}</td> <!-- PEP8 -->\n".format(total_fails)
                        else:
                            fails = 0
                            if row in list(items.keys()):
                                fails = items[row]
                            line = "\t\t\t\t<td>{}</td> <!-- PEP8 -->\n".format(fails)

                if "<tr" in line:
                    header = True
                elif "</tr>" in line:
                    if not found_entry:
                        if "Module" in row:
                            index.write("\t\t\t\t<th>PEP8</th>\n")
                        elif "Total" in row:
                            index.write("\t\t\t\t<td>{}</td> <!-- PEP8 -->\n".format(total_fails))
                        else:
                            fails = 0
                            if row in list(items.keys()):
                                fails = items[row]
                            index.write("\t\t\t\t<td>{}</td> <!-- PEP8 -->\n".format(fails))
                    found_entry = False
                index.write(line)
            index.close()


def pytest_runtest_logreport(report):
    global pep8
    if report.failed:
        if report.when == "call" and "PEP8-check" in report.location[2]:
            if not pep8:
                pep8 = open(".pep8rc", "w")
            pep8.write(report.location[0])
            pep8.write("\n")
            for line in report.longrepr.splitlines():
                if report.location[0] in line:
                    interest = line.split(report.location[0], 1)[1][1:]
                    pep8.write("\t{}".format(interest))
                    pep8.write("\n")
