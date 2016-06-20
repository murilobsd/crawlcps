# coding=utf-8

import os
import io
import sys
import json
import time
import urllib2
import hashlib
from bs4 import BeautifulSoup

from cps.gmail import Gmail


class CPS(object):
    folder = os.path.dirname(os.path.abspath(__file__))
    filenameconf = "conf.json"

    def __init__(self, conf_file=None):
        print "** Inciado Checagem de Vagas **"
        self.conf = self._config(conf_file)
        self.lasthash = None

    def _config(self, filename=None):
        """ carregando configuracoes """
        if filename:
            confpath = filename
        else:
            confpath = os.path.join(self.folder, self.filenameconf)

        if os.path.exists(confpath):
            with open(confpath) as data_file:
                return json.load(data_file)
        else:
            print "Nao existe arquivo de configuracao."
            sys.exit(0)

    def _get(self):
        """ requisicao """
        try:
            data = urllib2.urlopen(self.conf['url']).read()
            return data
        except:
            print "Erro ao conectar em %s" % self.url

    def _parse(self, data):
        """ parseando dados """
        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find("table", {"class": self.conf['classtable']})

        data = map(lambda x: x.findAll(text=True)[0],
                   table.findAll('td'))
        return data

    def _linhas(self, data):
        """ convertendo a lista para sring cada
            elemento uma nova linha"""
        return "\n".join(data)

    def check_vaga(self):
        """ checando se tem vaga """
        filename = os.path.join(self.folder, self.conf['backup'])

        while True:
            try:
                if not os.path.exists(filename):
                    data = self._get()
                    parse = self._parse(data)
                    self.lasthash = hashlib.md5(str(parse)).hexdigest()
                    self.salvar_dados(self._linhas(parse))
                else:
                    if not self.lasthash:
                        dadosantigos = self._linhas(self.carregando_dados())
                        self.lasthash = hashlib.md5(
                            dadosantigos.encode('utf-8')).hexdigest()
                    data = self._get()
                    parse = self._linhas(self._parse(data))
                    lasthash = hashlib.md5(parse.encode('utf-8')).hexdigest()
                    if lasthash != self.lasthash:
                        print "Existe algo novo"
                        self.enviar_notificacao()
                        self.salvar_dados(parse)
            except Exception as e:
                print "Error: %s" % e
                pass

            time.sleep(self.conf['periodo'])

    def salvar_dados(self, data):
        """ salvando dados"""
        filename = os.path.join(self.folder, self.conf['backup'])
        with io.open(filename, 'w', encoding='utf8') as f:
            f.write(data)

    def carregando_dados(self):
        """ carregando dados """
        filename = os.path.join(self.folder, self.conf['backup'])
        with io.open(filename, 'r', encoding='utf8') as f:
            return f.readlines()

    def enviar_notificacao(self):
        """ enviando notificacao para usuario """
        print "Enviando Notificacao."
        gm = Gmail(self.conf['email'], self.conf['password'])
        gm.send_message(self.conf['notificacao'],
                        'Notificacao Nova Vaga',  # Titulo
                        'Existe algo nova corra: %s' % self.conf['url'])
