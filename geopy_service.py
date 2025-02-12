from PySide6.QtWidgets import QDialog, QMessageBox, QProgressDialog
from PySide6.QtCore import Qt, QTimer
from ui_geopy_qt import Ui_GeoPy_Calculator
from geopy.distance import geodesic
import math
import folium
import csv
import simplekml
import webbrowser
from datetime import datetime
import json
import os

class GeoPyCalculator(QDialog):
    """
    Classe responsável por calcular e exibir informações geográficas
    baseadas em coordenadas fornecidas pelo usuário.
    """

    def __init__(self):
        """
        Inicializa a interface gráfica e conecta os botões aos métodos correspondentes.
        """
        super().__init__()
        self.ui = Ui_GeoPy_Calculator()
        self.ui.setupUi(self)
        
        # Conectar o botão calcular ao método
        self.ui.btnCalcular.clicked.connect(self.calcular)
        
        # Conectar o botão abrir mapa ao método
        self.ui.btnAbrirMapa.clicked.connect(self.abrir_mapa)
        
        # Conectar novo botão de ajuda
        self.ui.btnAjuda.clicked.connect(self.mostrar_ajuda)
        
        # Conectar novo botão de novo cálculo
        self.ui.btnNovo.clicked.connect(self.novo_calculo)
        
        # Conectar botão de mapa histórico
        self.ui.btnMapaHistorico.clicked.connect(self.abrir_mapa_historico)
        
        # Constantes
        self.RAIO_TERRA = 6371000  # Raio médio da Terra em metros
        
        # Carregar histórico
        self.historico = self.carregar_historico()
        
        self.progress = None

    def mostrar_progresso(self, titulo="Calculando...", texto="Processando dados"):
        """Cria e exibe um diálogo de progresso."""
        self.progress = QProgressDialog(texto, None, 0, 100, self)
        self.progress.setWindowTitle(titulo)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setMinimumDuration(0)
        self.progress.setValue(0)
        self.progress.setAutoClose(True)
        
    def atualizar_progresso(self, valor, texto=None):
        """Atualiza o valor e texto do diálogo de progresso."""
        if self.progress and texto:
            self.progress.setLabelText(texto)
        if self.progress:
            self.progress.setValue(valor)

    def calcular(self):
        """
        Realiza o cálculo das coordenadas do ponto alvo e exibe os resultados.
        """
        try:
            # Iniciar progresso
            self.mostrar_progresso()
            
            # Forçar delay inicial
            QTimer.singleShot(0, lambda: self.atualizar_progresso(10, "Validando entradas..."))
            QTimer.singleShot(400, lambda: self.processar_calculo())
            
        except Exception as e:
            if self.progress:
                self.progress.close()
            self.mostrar_resultado(f"Erro inesperado: {str(e)}")
    
    def processar_calculo(self):
        """Processa o cálculo com delays para mostrar o progresso."""
        try:
            # Obter valores dos campos
            lat_observador = float(self.ui.entry_lat_observador.text())
            lon_observador = float(self.ui.entry_lon_observador.text())
            altura = float(self.ui.entry_alt_observador.text())
            distancia = float(self.ui.entry_distancia.text())
            azimute = float(self.ui.entry_azimute.text())

            # Validações (400ms)
            QTimer.singleShot(400, lambda: self.atualizar_progresso(30, "Verificando limites..."))
            if not (-90 <= lat_observador <= 90) or not (-180 <= lon_observador <= 180):
                self.progress.close()
                self.mostrar_resultado("Erro: Latitude deve estar entre -90 e 90, e longitude entre -180 e 180.")
                return
            
            if not (0 <= azimute <= 360):
                self.progress.close()
                self.mostrar_resultado("Erro: O azimute deve estar entre 0 e 360 graus.")
                return
            
            if altura < 0 or distancia < 0:
                self.progress.close()
                self.mostrar_resultado("Erro: Altura e distância devem ser valores positivos.")
                return

            # Calcular coordenadas (400ms)
            QTimer.singleShot(800, lambda: self.atualizar_progresso(50, "Calculando coordenadas..."))
            lat_alvo, lon_alvo = self.calcular_coordenadas(lat_observador, lon_observador, 
                                                         altura, distancia, azimute)
            
            if lat_alvo is not None and lon_alvo is not None:
                # Calcular distâncias (400ms)
                QTimer.singleShot(1200, lambda: self.atualizar_progresso(70, "Calculando distâncias..."))
                distancia_horizonte = self.calcular_distancia_horizonte(altura)
                distancia_real = self.calcular_distancia_entre_pontos(
                    lat_observador, lon_observador, lat_alvo, lon_alvo)
                
                # Formatar resultado
                resultado = (f"Coordenadas do ponto alvo:\n"
                           f"Latitude: {lat_alvo:.6f}\n"
                           f"Longitude: {lon_alvo:.6f}\n"
                           f"Distância até o horizonte: {distancia_horizonte:.2f}m\n"
                           f"Distância entre pontos: {distancia_real:.2f}m")
                
                # Gerar arquivos (400ms)
                QTimer.singleShot(1600, lambda: self.atualizar_progresso(90, "Gerando arquivos..."))
                self.exibir_mapa(lat_observador, lon_observador, lat_alvo, lon_alvo)
                self.salvar_resultados_csv(lat_observador, lon_observador, 
                                         lat_alvo, lon_alvo, distancia_horizonte)
                self.salvar_kml(lat_observador, lon_observador, lat_alvo, lon_alvo)
                
                # Finalização (200ms)
                QTimer.singleShot(2000, lambda: self.finalizar_calculo(resultado))

        except ValueError:
            if self.progress:
                self.progress.close()
            self.mostrar_resultado("Erro: Entrada inválida. \nCertifique-se de digitar números válidos.")
        except Exception as e:
            if self.progress:
                self.progress.close()
            self.mostrar_resultado(f"Erro inesperado: {str(e)}")

    def finalizar_calculo(self, resultado):
        """Finaliza o cálculo mostrando o resultado."""
        self.atualizar_progresso(100, "Concluído!")
        QTimer.singleShot(100, self.progress.close)
        self.mostrar_resultado(resultado)

    def mostrar_resultado(self, texto):
        """
        Exibe o resultado ou mensagem de erro na interface.

        :param texto: Texto a ser exibido no label de resultado.
        """
        self.ui.label_resultado.setText(texto)

    def calcular_coordenadas(self, lat_observador, lon_observador, altura, distancia, azimute):
        """
        Calcula as coordenadas do ponto alvo com base nos dados fornecidos.

        :param lat_observador: Latitude do observador.
        :param lon_observador: Longitude do observador.
        :param altura: Altura do observador.
        :param distancia: Distância até o alvo.
        :param azimute: Azimute em graus.
        :return: Latitude e longitude do ponto alvo.
        """
        try:
            distancia_horizonte = self.calcular_distancia_horizonte(altura)
            if distancia > distancia_horizonte:
                self.mostrar_resultado(
                    f"Aviso: A distância informada ({distancia}m) é maior que "
                    f"a distância até o horizonte ({distancia_horizonte:.2f}m).")

            # Corrigir distância com altura (Teorema de Pitágoras)
            distancia_corrigida = math.sqrt(distancia**2 + altura**2)

            # Calcular nova posição
            ponto_inicial = (lat_observador, lon_observador)
            destino = geodesic(meters=distancia_corrigida).destination(ponto_inicial, azimute)
            return destino.latitude, destino.longitude
            
        except Exception as e:
            self.mostrar_resultado(f"Erro ao calcular coordenadas: {str(e)}")
            return None, None

    def calcular_distancia_horizonte(self, altura):
        """
        Calcula a distância até o horizonte com base na altura do observador.

        :param altura: Altura do observador.
        :return: Distância até o horizonte em metros.
        """
        return math.sqrt(2 * self.RAIO_TERRA * altura)

    def calcular_distancia_entre_pontos(self, lat1, lon1, lat2, lon2):
        """
        Calcula a distância geodésica entre dois pontos.

        :param lat1: Latitude do primeiro ponto.
        :param lon1: Longitude do primeiro ponto.
        :param lat2: Latitude do segundo ponto.
        :param lon2: Longitude do segundo ponto.
        :return: Distância entre os pontos em metros.
        """
        return geodesic((lat1, lon1), (lat2, lon2)).meters

    def exibir_mapa(self, lat_observador, lon_observador, lat_alvo, lon_alvo):
        """
        Gera e salva um mapa HTML com marcadores para o observador e o alvo.

        :param lat_observador: Latitude do observador.
        :param lon_observador: Longitude do observador.
        :param lat_alvo: Latitude do alvo.
        :param lon_alvo: Longitude do alvo.
        """
        # Gerar nome de arquivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_html = f"mapa_{timestamp}.html"
        
        mapa = folium.Map(location=[lat_observador, lon_observador], zoom_start=15)
        folium.Marker([lat_observador, lon_observador], tooltip="Observador").add_to(mapa)
        folium.Marker([lat_alvo, lon_alvo], tooltip="Alvo").add_to(mapa)
        folium.PolyLine([(lat_observador, lon_observador), 
                        (lat_alvo, lon_alvo)], color="red").add_to(mapa)
        mapa.save(arquivo_html)
        return arquivo_html

    def salvar_resultados_csv(self, lat_observador, lon_observador, 
                            lat_alvo, lon_alvo, distancia_horizonte, 
                            arquivo="resultados.csv"):
        """Salva os resultados incluindo data e hora."""
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Gerar nomes de arquivos
        arquivo_kml = self.salvar_kml(lat_observador, lon_observador, lat_alvo, lon_alvo)
        arquivo_html = self.exibir_mapa(lat_observador, lon_observador, lat_alvo, lon_alvo)
        
        # Criar cabeçalho se o arquivo não existir
        if not os.path.exists(arquivo):
            with open(arquivo, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Data/Hora", "Latitude Observador", 
                               "Longitude Observador", "Latitude Alvo", 
                               "Longitude Alvo", "Distância Horizonte (m)",
                               "Arquivo KML", "Arquivo HTML"])
        
        # Adicionar nova linha
        with open(arquivo, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([data_hora, lat_observador, lon_observador,
                           lat_alvo, lon_alvo, distancia_horizonte,
                           arquivo_kml, arquivo_html])
        
        # Atualizar histórico
        self.historico.append({
            "data_hora": data_hora,
            "lat_observador": lat_observador,
            "lon_observador": lon_observador,
            "lat_alvo": lat_alvo,
            "lon_alvo": lon_alvo,
            "distancia_horizonte": distancia_horizonte,
            "arquivo_kml": arquivo_kml,
            "arquivo_html": arquivo_html
        })
        self.salvar_historico()

    def salvar_kml(self, lat_observador, lon_observador, 
                  lat_alvo, lon_alvo):
        """
        Salva os resultados do cálculo em um arquivo KML.

        :param lat_observador: Latitude do observador.
        :param lon_observador: Longitude do observador.
        :param lat_alvo: Latitude do alvo.
        :param lon_alvo: Longitude do alvo.
        """
        # Gerar nome de arquivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_kml = f"resultado_{timestamp}.kml"
        
        kml = simplekml.Kml()
        
        ponto_obs = kml.newpoint(name="Observador")
        ponto_obs.coords = [(lon_observador, lat_observador)]
        ponto_obs.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/grn-circle.png'
        
        ponto_alvo = kml.newpoint(name="Alvo")
        ponto_alvo.coords = [(lon_alvo, lat_alvo)]
        ponto_alvo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'
        
        linha = kml.newlinestring(name="Linha de Visada")
        linha.coords = [(lon_observador, lat_observador), (lon_alvo, lat_alvo)]
        linha.style.linestyle.width = 2
        linha.style.linestyle.color = simplekml.Color.red
        
        kml.save(arquivo_kml)
        return arquivo_kml

    def abrir_mapa(self):
        """
        Abre o arquivo HTML do mapa no navegador padrão.
        """
        try:
            webbrowser.open("mapa.html")
        except Exception as e:
            self.mostrar_resultado(f"Erro ao abrir o mapa: {str(e)}")

    def mostrar_ajuda(self):
        """Exibe uma janela de ajuda com instruções básicas."""
        texto_ajuda = """
        Como usar o Calculador GeoPy:
        
        1. Latitude/Longitude: Digite em graus decimais
           Ex: -23.5505 (Sul) ou 45.5017 (Norte)
        
        2. Altura: Digite em metros
        
        3. Distância: Digite em metros até o alvo
        
        4. Azimute: Digite em graus (0-360)
           0° = Norte
           90° = Leste
           180° = Sul
           270° = Oeste
        
        Os resultados serão salvos automaticamente
        e podem ser encontrados em 'resultados.csv'
        """
        QMessageBox.information(self, "Ajuda", texto_ajuda)

    def novo_calculo(self):
        """Limpa todos os campos de entrada e o resultado."""
        # Limpar campos de entrada
        self.ui.entry_lat_observador.clear()
        self.ui.entry_lon_observador.clear()
        self.ui.entry_alt_observador.clear()
        self.ui.entry_distancia.clear()
        self.ui.entry_azimute.clear()
        
        # Limpar resultado
        self.ui.label_resultado.setText("")
        
        # Colocar foco no primeiro campo
        self.ui.entry_lat_observador.setFocus()

    def carregar_historico(self):
        """Carrega o histórico de cálculos do arquivo JSON."""
        try:
            if os.path.exists("historico.json"):
                with open("historico.json", "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def salvar_historico(self):
        """Salva o histórico de cálculos em um arquivo JSON."""
        try:
            with open("historico.json", "w") as f:
                json.dump(self.historico, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")

    def gerar_mapa_historico(self, arquivo_historico="historico.json", arquivo_mapa="mapa_historico.html"):
        """
        Gera um mapa HTML com todos os pontos registrados no histórico.

        :param arquivo_historico: Nome do arquivo JSON contendo o histórico.
        :param arquivo_mapa: Nome do arquivo HTML a ser gerado.
        """
        try:
            # Carregar histórico
            with open(arquivo_historico, "r") as f:
                historico = json.load(f)

            # Criar mapa centrado no primeiro ponto do histórico
            if historico:
                primeiro_ponto = historico[0]
                mapa = folium.Map(location=[primeiro_ponto["lat_observador"], primeiro_ponto["lon_observador"]], zoom_start=10)

                # Adicionar marcadores para cada ponto no histórico
                for entrada in historico:
                    folium.Marker(
                        [entrada["lat_observador"], entrada["lon_observador"]],
                        tooltip="Observador",
                        icon=folium.Icon(color="green")
                    ).add_to(mapa)
                    folium.Marker(
                        [entrada["lat_alvo"], entrada["lon_alvo"]],
                        tooltip="Alvo",
                        icon=folium.Icon(color="red")
                    ).add_to(mapa)
                    folium.PolyLine(
                        [(entrada["lat_observador"], entrada["lon_observador"]),
                         (entrada["lat_alvo"], entrada["lon_alvo"])],
                        color="blue"
                    ).add_to(mapa)

                # Salvar mapa
                mapa.save(arquivo_mapa)
                print(f"Mapa gerado com sucesso: {arquivo_mapa}")
            else:
                print("Histórico vazio. Nenhum mapa gerado.")

        except Exception as e:
            print(f"Erro ao gerar mapa do histórico: {e}")

    def abrir_mapa_historico(self):
        """Gera e abre o mapa histórico no navegador."""
        try:
            # Mostrar diálogo de progresso
            self.mostrar_progresso("Gerando Mapa Histórico", "Processando dados do histórico...")
            
            # Gerar nome único para o arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_mapa = f"mapa_historico_{timestamp}.html"
            
            # Gerar o mapa
            self.gerar_mapa_historico(arquivo_mapa=arquivo_mapa)
            
            # Fechar progresso
            if self.progress:
                self.progress.close()
            
            # Abrir o mapa no navegador
            webbrowser.open(arquivo_mapa)
            
        except Exception as e:
            if self.progress:
                self.progress.close()
            QMessageBox.warning(self, "Erro", f"Erro ao gerar mapa histórico: {str(e)}")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = GeoPyCalculator()
    window.show()
    sys.exit(app.exec())
