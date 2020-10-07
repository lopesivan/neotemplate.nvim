import sys
import os
import glob
import StringIO
from Cheetah.Template import Template

import neovim


@neovim.plugin
class CheetahPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    def get_line(self, file):
        fp = open(file)
        for i, line in enumerate(fp):
            if i == 2:
                self.nvim.out_write(line)
                break
        fp.close()

    def load_cheetah_tmpl(self, name, range, args, tmpl):

        if len(args) == 2:
            if args[1] == "--help":
                self.get_line(os.path.expandvars(tmpl))
            else:
                view = os.path.expandvars(tmpl)
                dataout = Template(open(view).read(), searchList=[{'name': name,
                                                                   'data': args}])
                r = self.nvim.current.buffer.range(int(range[0]), int(range[1]))
                redirected = StringIO.StringIO()
                sys.stdout = redirected
                print(dataout)
                sys.stdout = sys.__stdout__
                output = redirected.getvalue().split('\n')
                r[:] = output[:-2]  # the -1 is to remove the final blank line
                redirected.close()
        else:
            view = os.path.expandvars(tmpl)
            dataout = Template(open(view).read(), searchList=[{'name': name,
                                                               'data': args}])
            r = self.nvim.current.buffer.range(int(range[0]), int(range[1]))
            redirected = StringIO.StringIO()
            sys.stdout = redirected
            print(dataout)
            sys.stdout = sys.__stdout__
            output = redirected.getvalue().split('\n')
            r[:] = output[:-2]  # the -1 is to remove the final blank line
            redirected.close()

    @neovim.command("Template", complete='customlist,CompleteTemplates', range='', nargs='*')
    def neotemplate(self, args, range):

        if len(args) == 0:
            self.nvim.out_write("Template [argument]" + "\n")
        else:
            name     = self.nvim.current.buffer.name
            filetype = self.nvim.eval("&ft")

            if (filetype == ""):
                extension = name.split(".")[-1]
                filetype  = extension

            tmpl = ("$HOME/.config/nvim/cheetah/tmpl/{}/{}.cheetah"
                    .format(filetype, args[0].lower()))

            if name.split("/")[-1] == "Dockerfile":
                tmpl = ("$HOME/.config/nvim/cheetah/tmpl/{}/{}.cheetah"
                    .format("dockerfile", "Dockerfile"))

            if name.split("/")[-1] == "Makefile":
                tmpl = ("$HOME/.config/nvim/cheetah/tmpl/{}/{}.cheetah"
                    .format("mk", args[0].lower()))

            self.load_cheetah_tmpl(name, range, args, tmpl)
