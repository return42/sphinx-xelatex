# -*- coding: utf-8; mode: python -*-

"""
    xelatex_ext.builders.xelatex
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    XeLaTeX builder.

    :copyright:  Copyright (C) 2016 Markus Heiser
    :license:    GPL V3.0, see LICENSE for details.

    TODO: document ...

    * XeLaTex does not use sphinx.sty, has it's own "xetex_inputs" folder with an
      other set of files needed for a XeTeX run.

"""

# ==============================================================================
# imports
# ==============================================================================

from os import path, listdir
from six import iteritems

from docutils import nodes
from docutils.io import FileOutput
from docutils.utils import new_document

from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.environment import NoUri
from sphinx.errors import SphinxError
from sphinx.util.console import bold, darkgreen
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.osutil import copyfile
from sphinx.util.parallel import ParallelTasks, make_chunks

from xelatex_ext.writers.doccfg import XeLaTeXDocSet
from xelatex_ext.writers.xelatex import XeLaTeXWriter

XETEX_INPUTS_FOLDER = path.abspath(
    path.join(path.dirname(__file__), "xetex_inputs"))

# ==============================================================================
class XeLaTeXBuilder(Builder):
# ==============================================================================

    name        = 'xelatex'
    format      = 'xelatex'
    writerClass = XeLaTeXWriter

    # allow parallel write_doc() calls
    allow_parallel = True

    supported_image_types = [
        'application/pdf'
        , 'application/eps'
        , 'image/png'
        , 'image/gif'
        , 'image/jpeg'
        ]

    def init(self):

        u"""XeLaTeXBuilder specific initialisations.

        Init / set required members.

        :ivar XeLateXDocSet docset:  Extended (Xe)LaTeX *per-document* settings.
        """
        super(XeLaTeXBuilder, self).init()
        self.docset = XeLaTeXDocSet(self.app)

    def get_outdated_docs(self):
        u"""Allways returns *all documents*

        Partial (re-) build of (Xe)LaTeX output is not intended!  """

        return 'all documents'  # for now

    def build(self, docnames, summary=None, _method=None):
        u"""Build (Xe)LaTeX documents.

        Builds always all (Xe)LaTeX documents.  Partial (re-) build of (Xe)LaTeX
        output is not yet intended.  (see :py:`meth`get_outdated_docs`)."""

        super(XeLaTeXBuilder, self).build(docnames, summary=summary, method=None)

    def prepare_writing(self, docCfgList):
        """A place where you can add logic before :meth:`write_doc` is run"""
        pass

    def write(self, *_ignored):
        if not self.docset.docs:
            self.info(bold('no XeLaTeX targets to build'))
            return

        self.info(bold('preparing targets... '), nonl=True)
        self.prepare_writing(self.docset.docs)
        self.info('done')

        warnings = []
        self.env.set_warnfunc(
            lambda *args, **kwargs: warnings.append((args, kwargs)))
        if self.parallel_ok:
            # number of subprocesses is parallel-1 because the main process
            # is busy loading doctrees and doing write_doc_serialized()
            self._write_parallel(
                self.docset.docs, warnings, nproc=self.app.parallel - 1)
        else:
            self._write_serial(self.docset.docs, warnings)
        self.env.set_warnfunc(self.warn)

    def _write_serial(self, docCfgList, warnings):
        for docCfg in self.app.status_iterator(
                docCfgList, 'writing output... ', darkgreen, len(docCfgList)):
            self.write_doc_serialized(docCfg)
            self.write_doc(docCfg)
        for warning, kwargs in warnings:
            self.warn(*warning, **kwargs)

    def _write_parallel(self, docCfgList, warnings, nproc):
        def write_process(docs):
            local_warnings = []
            def warnfunc(*args, **kwargs):
                local_warnings.append((args, kwargs))
            self.env.set_warnfunc(warnfunc)
            for targetname, doctree in docs:
                self.write_doc(targetname, doctree)
            return local_warnings

        def add_warnings(_docs, wlist):
            warnings.extend(wlist)

        # warm up caches/compile templates using the first document
        docCfg, docCfgList = docCfgList[0], docCfgList[1:]

        self.write_doc_serialized(docCfg)
        self.write_doc(docCfg)

        tasks  = ParallelTasks(nproc)
        chunks = make_chunks(docCfg, nproc)

        for chunk in self.app.status_iterator(
                chunks, 'writing output... ', darkgreen, len(chunks)):
            arg = []
            for docCfg in chunk:
                self.write_doc_serialized(docCfg)
                arg.append((docCfg,))
            tasks.add_task(write_process, arg, add_warnings)

        # make sure all threads have finished
        self.info(bold('waiting for workers...'))
        tasks.join()

        for warning, kwargs in warnings:
            self.warn(*warning, **kwargs)

    def write_doc_serialized(self, docCfg):  # pylint: disable=W0221
        """Handle parts of write_doc that must be called in the main process
        if parallel build is active.
        """
        pass

    def write_doc(self, docCfg):  # pylint: disable=W0221
        """Where you actually write something to the filesystem.
        """
        self.info("processing " + docCfg.targetname + "... ", nonl=1)

        # The argument doctree are covered by the self.assemble_doctree
        # method. The docCfg is shipped in the writer.document.docCfg

        doctree = self.assemble_doctree(docCfg)
        doctree.docCfg = docCfg

        self.post_process_images(doctree)
        self.info("writing... ", nonl=1)
        outFile = FileOutput(
            destination_path = path.join(self.outdir, docCfg.targetname)
            , encoding       = 'utf-8')

        writer = self.writerClass(self)
        writer.write(doctree , outFile)
        self.info("done")

    def assemble_doctree(self, docCfg):

        self.info(darkgreen(docCfg.docname))
        tree = self.env.get_doctree(docCfg.docname)

        if docCfg.toctree_only:
            # extract toctree nodes from the tree and put them in a
            # fresh document
            new_tree = new_document('<latex output>')
            new_sect = nodes.section()
            new_sect += nodes.title(
                u'<Set title in conf.py>', u'<Set title in conf.py>')
            new_tree += new_sect
            for node in tree.traverse(addnodes.toctree):
                new_sect += node
            tree = new_tree

        tree = inline_all_toctrees(
            self, self.docset.docnames, docCfg.docname, tree
            , darkgreen, [docCfg.docname])

        tree['docname'] = docCfg.docname

        for appendix_docname in docCfg.appendices:
            appendix = self.env.get_doctree(appendix_docname)
            appendix['docname'] = appendix_docname
            tree.append(appendix)

        self.info("resolving references...")
        self.env.resolve_references(tree, docCfg.docname, self)
        docCfg.replacePendingRefsInTree(tree)
        docCfg.initFromTree(tree)
        return tree

    def get_target_uri(self, docname, typ=None):
        """Return the target URI for a document name."""
        if docname not in self.docset.docnames:
            raise NoUri
        else:
            return '%' + docname

    def get_relative_uri(self, from_, to, typ=None):
        """Return a relative URI between two source filenames.

        This implementation always ignores the *from* path.  May raise
        environment.NoUri if there's no way to return a sensible URI."""
        return self.get_target_uri(to, typ)

    def finish(self):
        # copy image files
        if self.images:
            self.info(bold('copying images...'), nonl=1)
            for src, dst in iteritems(self.images):
                self.info(' ' + src, nonl=1)
                src = path.join(self.srcdir, src)
                dst = path.join(self.outdir, dst)
                copyfile(src, dst)
            self.info()

        # copy XeTeX support files from texinputs
        self.info(bold('copying XeTeX support files...'))
        for fname in listdir(XETEX_INPUTS_FOLDER):
            if not fname.startswith('.'):
                src = path.join(XETEX_INPUTS_FOLDER, fname)
                dst = path.join(self.outdir, fname)
                copyfile(src, dst)

        # copy additional files
        if self.docset.additional_files:
            self.info(bold('copying additional files...'), nonl=1)
            _copied = []
            for fname in self.docset.additional_files:
                self.info(' ' + fname, nonl=1)
                src = path.join(self.confdir, fname)
                dst = path.join(self.outdir, path.basename(fname))
                if dst in _copied:
                    raise SphinxError(
                        "two *additional* files with same basename `%s`"
                        % path.basename(fname))
                copyfile(src, dst)
            self.info()

        # copy logo
        if self.docset.logo:
            fname = path.basename(self.docset.logo)
            src   = path.join(self.confdir, fname)
            dst   = path.join(self.outdir, fname)
            if not path.isfile(src):
                raise SphinxError('logo file %r does not exist' % src)
            elif not path.isfile(dst):
                copyfile(src, dst)

        # all done
        self.info('done')
