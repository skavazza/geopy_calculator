from PySide6.QtWidgets import QApplication
from geopy_service import GeoPyCalculator
import sys

def main():
    """
    Função principal que inicializa a aplicação Qt e exibe a janela principal.
    """
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = GeoPyCalculator()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())