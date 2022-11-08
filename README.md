# MÓDULO DE TEMPERATURA

Projeto do sensor de temperatura, com o sensor do tipo PT100 de 4 fios, um módulo MAX31865 conversor do sinal para comunicação SPI com a placa Raspberry Pi Pico e com a visualização dos dados em um Display Nokia 5110. 

Foi utilizado o VS Code junto com o MicroPython para programar o microcontrolador. O arquivo main.py executa um loop, que executa a leitura do sensor, e devolve alguns parâmetros como a temperatura e o valor de resistência medido pelo PT100. O arquivo MAX31865 contém a conversão da leitura do valor lido pelo módulo para seu respectivo valor de temperatura associado, nele são definidos como parâmetro de entrada o número dos pinos GPIO utilizados.

Além disso, o projeto contém os arquivos Altium para criação da placa de 2 faces do projeto e os arquivos Gerber e NC Drill para sua fabricação na pasta de "Outputs". Datasheets e documentos de referência também estão anexados no projeto.


<p align="center">
  <img src="https://github.com/open-weather-iot/temperature-module/blob/main/Projeto.jpg" width="350" alt="accessibility text">
</p>
<p align="center">
  <img src="https://github.com/open-weather-iot/temperature-module/blob/main/schematic.png" width="400" alt="accessibility text">
</p>
