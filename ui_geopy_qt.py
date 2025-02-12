# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'geopy_qtxgLDcc.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication,
    QMetaObject, QRect)
from PySide6.QtWidgets import (QGroupBox, QLabel,
    QLineEdit, QPushButton)


class Ui_GeoPy_Calculator(object):
    def setupUi(self, GeoPy_Calculator):
        if not GeoPy_Calculator.objectName():
            GeoPy_Calculator.setObjectName(u"GeoPy_Calculator")
        GeoPy_Calculator.resize(600, 257)
        self.cbResultado = QGroupBox(GeoPy_Calculator)
        self.cbResultado.setObjectName(u"cbResultado")
        self.cbResultado.setGeometry(QRect(312, 30, 270, 191))
        self.label_resultado = QLabel(self.cbResultado)
        self.label_resultado.setObjectName(u"label_resultado")
        self.label_resultado.setGeometry(QRect(18, 49, 230, 101))
        self.btnCalcular = QPushButton(GeoPy_Calculator)
        self.btnCalcular.setObjectName(u"btnCalcular")
        self.btnCalcular.setGeometry(QRect(20, 210, 131, 31))
        self.btnAbrirMapa = QPushButton(GeoPy_Calculator)
        self.btnAbrirMapa.setObjectName(u"btnAbrirMapa")
        self.btnAbrirMapa.setGeometry(QRect(160, 210, 131, 31))
        self.label_lat_observador = QLabel(GeoPy_Calculator)
        self.label_lat_observador.setObjectName(u"label_lat_observador")
        self.label_lat_observador.setGeometry(QRect(20, 40, 141, 16))
        self.label_lon_observador = QLabel(GeoPy_Calculator)
        self.label_lon_observador.setObjectName(u"label_lon_observador")
        self.label_lon_observador.setGeometry(QRect(20, 70, 141, 16))
        self.label_alt_observador = QLabel(GeoPy_Calculator)
        self.label_alt_observador.setObjectName(u"label_alt_observador")
        self.label_alt_observador.setGeometry(QRect(20, 100, 141, 16))
        self.label_dist_alvo = QLabel(GeoPy_Calculator)
        self.label_dist_alvo.setObjectName(u"label_dist_alvo")
        self.label_dist_alvo.setGeometry(QRect(20, 130, 141, 16))
        self.label_azimute = QLabel(GeoPy_Calculator)
        self.label_azimute.setObjectName(u"label_azimute")
        self.label_azimute.setGeometry(QRect(20, 160, 141, 16))
        self.entry_lat_observador = QLineEdit(GeoPy_Calculator)
        self.entry_lat_observador.setObjectName(u"entry_lat_observador_2")
        self.entry_lat_observador.setGeometry(QRect(160, 40, 113, 22))
        self.entry_lon_observador = QLineEdit(GeoPy_Calculator)
        self.entry_lon_observador.setObjectName(u"entry_lon_observador")
        self.entry_lon_observador.setGeometry(QRect(160, 70, 113, 22))
        self.entry_alt_observador = QLineEdit(GeoPy_Calculator)
        self.entry_alt_observador.setObjectName(u"entry_alt_observador")
        self.entry_alt_observador.setGeometry(QRect(160, 100, 113, 22))
        self.entry_distancia = QLineEdit(GeoPy_Calculator)
        self.entry_distancia.setObjectName(u"entry_distancia")
        self.entry_distancia.setGeometry(QRect(160, 130, 113, 22))
        self.entry_azimute = QLineEdit(GeoPy_Calculator)
        self.entry_azimute.setObjectName(u"entry_azimute")
        self.entry_azimute.setGeometry(QRect(160, 160, 113, 22))
        
        # Adicionando placeholders
        self.entry_lat_observador.setPlaceholderText(u"Ex: -23.5505")
        self.entry_lon_observador.setPlaceholderText(u"Ex: -46.6333")
        self.entry_alt_observador.setPlaceholderText(u"Ex: 100 (metros)")
        self.entry_distancia.setPlaceholderText(u"Ex: 1000 (metros)")
        self.entry_azimute.setPlaceholderText(u"Ex: 90 (graus)")
        
        # Adicionando botão de ajuda
        self.btnAjuda = QPushButton(GeoPy_Calculator)
        self.btnAjuda.setObjectName(u"btnAjuda")
        self.btnAjuda.setGeometry(QRect(20, 10, 75, 24))
        
        # Adicionando botão Novo Cálculo
        self.btnNovo = QPushButton(GeoPy_Calculator)
        self.btnNovo.setObjectName(u"btnNovo")
        self.btnNovo.setGeometry(QRect(105, 10, 100, 24))
        
        # Adicionando botão Mapa Histórico
        self.btnMapaHistorico = QPushButton(GeoPy_Calculator)
        self.btnMapaHistorico.setObjectName(u"btnMapaHistorico")
        self.btnMapaHistorico.setGeometry(QRect(215, 10, 100, 24))

        self.retranslateUi(GeoPy_Calculator)

        QMetaObject.connectSlotsByName(GeoPy_Calculator)
    # setupUi

    def retranslateUi(self, GeoPy_Calculator):
        GeoPy_Calculator.setWindowTitle(QCoreApplication.translate("GeoPy_Calculator", u"Dialog", None))
        self.cbResultado.setTitle(QCoreApplication.translate("GeoPy_Calculator", u"Resultado", None))
        self.label_resultado.setText("")
        self.btnCalcular.setText(QCoreApplication.translate("GeoPy_Calculator", u"Calcular", None))
        self.btnAbrirMapa.setText(QCoreApplication.translate("GeoPy_Calculator", u"Abrir Mapa", None))
        self.label_lat_observador.setText(QCoreApplication.translate("GeoPy_Calculator", u"Latitude do Observador", None))
        self.label_lon_observador.setText(QCoreApplication.translate("GeoPy_Calculator", u"Longitude do Observador", None))
        self.label_alt_observador.setText(QCoreApplication.translate("GeoPy_Calculator", u"Altura do Observador", None))
        self.label_dist_alvo.setText(QCoreApplication.translate("GeoPy_Calculator", u"Dist\u00e2ncia at\u00e9 o alvo", None))
        self.label_azimute.setText(QCoreApplication.translate("GeoPy_Calculator", u"Azimute em graus", None))
        self.btnAjuda.setText(QCoreApplication.translate("GeoPy_Calculator", u"Ajuda", None))
        self.btnNovo.setText(QCoreApplication.translate("GeoPy_Calculator", u"Novo Cálculo", None))
        self.btnMapaHistorico.setText(QCoreApplication.translate("GeoPy_Calculator", u"Mapa Histórico", None))
    # retranslateUi

