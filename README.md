# GeoPy Calculator

## Descrição
O GeoPy Calculator é uma aplicação desktop desenvolvida em Python que permite calcular coordenadas geográficas de um ponto alvo com base na posição do observador, distância e azimute.

## Funcionalidades
- Cálculo de coordenadas geográficas (latitude/longitude) do ponto alvo
- Visualização dos resultados em mapa interativo
- Histórico de cálculos realizados
- Exportação de resultados em formatos KML e CSV
- Interface gráfica intuitiva

## Pré-requisitos
- Python 3.8 ou superior
- PySide6
- Folium
- Pandas
- GeoPy

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/GeoPy-Calculator.git
   cd GeoPy-Calculator
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como usar
1. Execute o arquivo principal:
   ```bash
   python main.py
   ```

2. Na interface do programa:
   - Insira a latitude do observador (ex: -23.5505)
   - Insira a longitude do observador (ex: -46.6333)
   - Informe a altura do observador em metros
   - Digite a distância até o alvo em metros
   - Informe o azimute em graus (0-360)
   - Clique em "Calcular" para obter o resultado

## Recursos adicionais
- Botão "Ajuda" para informações sobre como usar a aplicação
- Botão "Novo Cálculo" para limpar os campos
- Botão "Mapa Histórico" para visualizar cálculos anteriores
- Exportação automática dos resultados em KML para uso em aplicações GIS

## Contribuição
Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Contato
Seu Nome - seu.email@exemplo.com
Link do projeto: https://github.com/seu-usuario/geopy-calculator

