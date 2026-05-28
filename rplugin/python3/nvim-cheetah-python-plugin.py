# -*- coding: utf-8 -*-

import sys
import os
import io

from Cheetah.Template import Template

import neovim


@neovim.plugin
class CheetahPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    def get_line(self, filename):
        try:
            with open(filename, "r") as fp:
                for i, line in enumerate(fp):
                    if i == 2:
                        self.nvim.out_write(line)
                        return
        except FileNotFoundError:
            self.nvim.err_write("Arquivo não encontrado: {}\n".format(filename))

    def render_template(self, name, args, tmpl):
        view = os.path.expandvars(tmpl)

        if not os.path.isfile(view):
            self.nvim.err_write("Template não encontrado: {}\n".format(view))
            return None

        with open(view, "r") as fp:
            template_source = fp.read()

        dataout = Template(
            template_source,
            searchList=[
                {
                    "name": name,
                    "data": args,
                }
            ],
        )

        redirected = io.StringIO()

        old_stdout = sys.stdout

        try:
            sys.stdout = redirected
            print(dataout)
        finally:
            sys.stdout = old_stdout

        output = redirected.getvalue().split("\n")
        redirected.close()

        return output[:-2]

    def load_cheetah_tmpl(self, name, range, args, tmpl):
        view = os.path.expandvars(tmpl)

        if len(args) == 2 and args[1] == "--help":
            self.get_line(view)
            return

        output = self.render_template(name, args, tmpl)

        if output is None:
            return

        r = self.nvim.current.buffer.range(
            int(range[0]),
            int(range[1])
        )

        r[:] = output

    @neovim.command(
        "Template",
        complete="customlist,CompleteTemplates",
        range="",
        nargs="*",
    )
    def neotemplate(self, args, range):
        if len(args) == 0:
            self.nvim.out_write("Template [argument]\n")
            return

        name = self.nvim.current.buffer.name
        filetype = self.nvim.eval("&ft")

        if filetype == "":
            extension = name.split(".")[-1]
            filetype = extension

        basename = name.split("/")[-1]

        tmpl = "$NDE_APP_CONFIG/cheetah/tmpl/{}/{}.cheetah".format(
            filetype,
            args[0].lower(),
        )

        if basename == "Dockerfile":
            tmpl = "$NDE_APP_CONFIG/cheetah/tmpl/{}/{}.cheetah".format(
                "dockerfile",
                "Dockerfile",
            )

        if basename == "Makefile":
            tmpl = "$NDE_APP_CONFIG/cheetah/tmpl/{}/{}.cheetah".format(
                "mk",
                args[0].lower(),
            )

        self.load_cheetah_tmpl(name, range, args, tmpl)
