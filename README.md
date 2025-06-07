<h1 align="center">🔎 License Plate Recognition</h1>

<p align="center">
  <img src="https://img.shields.io/github/stars/DiogoGaspar6/license-plate-recognition?style=social" alt="GitHub stars"/>
  <img src="https://img.shields.io/github/forks/DiogoGaspar6/license-plate-recognition?style=social" alt="GitHub forks"/>
  <img src="https://img.shields.io/github/issues/DiogoGaspar6/license-plate-recognition" alt="Issues abertas"/>
  <img src="https://img.shields.io/github/issues-pr/DiogoGaspar6/license-plate-recognition" alt="Pull Requests abertos"/>
  <img src="https://img.shields.io/github/last-commit/DiogoGaspar6/license-plate-recognition" alt="Último commit"/>
  <img src="https://img.shields.io/github/license/DiogoGaspar6/license-plate-recognition" alt="Licença"/>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python"/>
</p>

<p align="center">
  <b>Reconhecimento e deteção automática de matrículas portuguesas usando Python, YOLO e EasyOCR.</b>
</p>

---

## 📖 Descrição

Este projeto utiliza o modelo YOLO para deteção de matrículas em imagens e o EasyOCR para reconhecimento dos caracteres. Quando uma matrícula portuguesa é detetada com alta confiança, a imagem da matrícula é guardada na pasta `detected_license_plates` e a informação extraída é registada no ficheiro Excel `license_plates.xlsx`.

---

## 🚀 Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/DiogoGaspar6/license-plate-recognition.git
   cd license-plate-recognition
   ```

2. Instale as dependências:
   ```sh
   pip install -r src/requirements.txt
   ```

---

## ⚡️ Como Usar

Execute o script principal:
```sh
python3 src/main.py
```

- As imagens das matrículas detetadas serão guardadas em `src/detected_license_plates/`.
- Os dados das matrículas reconhecidas serão adicionados ao ficheiro `src/license_plates.xlsx`.

---

## 📝 Estrutura do Projeto

```
license-plate-recognition/
│
├── src/
│   ├── main.py
│   ├── test.py
│   ├── requirements.txt
│   ├── license_plates.xlsx
│   └── detected_license_plates/
├── models/
├── runs/
├── README.md
├── .gitignore
└── ...
```

---

## 👤 Autor

- **Diogo Gaspar**
  - [GitHub](https://github.com/DiogoGaspar6)
  - [LinkedIn](https://linkedin.com/in/diogoogaspar)

---

## ⭐️ Mostre seu apoio

Se este projeto foi útil para você, deixe uma estrela ⭐️ no repositório!

---

## 🛠️ Tecnologias

- Python
- YOLO
- EasyOCR
