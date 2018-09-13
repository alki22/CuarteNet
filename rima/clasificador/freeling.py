# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

from subprocess import PIPE, Popen

if sys.version_info.major == 2:
    from distutils.spawn import find_executable as which
else:
    from shutil import which


_INPUT_FORMATS = {'text', 'freeling', 'conll'}
_INPUT_LEVELS = {'text', 'token', 'splitted', 'morfo', 'tagged', 'shallow', 'dep'}
_OUTPUT_FORMATS = {'freeling', 'conll', 'xml', 'json', 'naf', 'train'}
_OUTPUT_LEVELS = {'ident', 'token', 'splitted', 'morfo', 'tagged', 'shallow',
                  'parsed', 'dep', 'coref', 'semgraph'}
_LANGUAGES = {'as', 'es', 'ca', 'en', 'cy', 'it', 'gl', 'pt', 'ru'}
_SENSE = {'all', 'mfs', 'ukb'}


class Freeling(object):
    """Wrapper for calling the analyze script of the FreeLing tool suite"""

    _freeling_cmd = 'analyze'

    def __init__(self, language=None, input_format='text', input_level='text',
                 output_format='freeling', output_level='tagged', multiword=True,
                 ner=True, nec=False, sense=None, config_file_path=None):
        assert (language is not None and language in _LANGUAGES) or config_file_path is not None, \
            'Either language or the config file path should be given. Language must be one of %s' % _LANGUAGES

        assert input_format in _INPUT_FORMATS, 'Input format must be one of %s' % _INPUT_FORMATS
        assert input_level in _INPUT_LEVELS, 'Input level must be one of %s' % _INPUT_LEVELS
        assert output_format in _OUTPUT_FORMATS, 'Output format must be one of %s' % _OUTPUT_FORMATS
        assert output_level in _OUTPUT_LEVELS, 'Output level must be one of %s' % _OUTPUT_LEVELS

        assert sense is None or sense in _SENSE, 'Sense must be one of %s' % _SENSE

        self._language = language
        self._input_format = input_format
        self._input_level = input_level
        self._output_format = output_format
        self._output_level = output_level
        self._multiword = multiword
        self._ner = ner
        self._nec = nec
        self._sense = sense

        self._config_file_path = config_file_path

    def _build_command(self):
        cmd = [which(self._freeling_cmd)]

        # Either use the config file
        if self._config_file_path is not None:
            cmd.append('-f %s' % os.path.abspath(self._config_file_path))
        else:
            cmd.append('-f %s.cfg' % self._language)
            cmd.append('--input %s' % self._input_format)
            cmd.append('--inplv %s' % self._input_level)
            cmd.append('--output %s' % self._output_format)
            cmd.append('--outlv %s' % self._output_level)

            cmd.append('--loc' if self._multiword else '--noloc')

            cmd.append('--ner' if self._ner else '--noner')
            cmd.append('--nec' if self._nec else '--nonec')

            if self._sense:
                cmd.append('--sense %s' % self._sense)

        return cmd

    def run(self, sentences):
        """
        Run analyzer script according to the options given in the constructor.
        :param sentence: Sentence to parse. Should be in the right format. Either as a list
            or as a string with the correct new lines (if there is any).
        :return: Output and error of the analyzer script.
        """

        assert sentences != [], 'The given sentence must be a string or a non empty list'

        process = Popen(self._build_command(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        if isinstance(sentences, list) and isinstance(sentences[0], list):
            sentences = '\n\n'.join('\n'.join(sentence) for sentence in sentences)
        elif isinstance(sentences, list):
            sentences = '\n'.join(sentences)
        sentences += '\n\n'

        return process.communicate(sentences.encode('utf-8')), process.returncode