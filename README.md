# IA a Serviço da Inclusão – Tecnologia para Todos

Site educativo sobre tecnologia assistiva e inclusão, com assistente virtual, busca de tecnologias e prancha de comunicação. Feito com **HTML, CSS, JavaScript e Python (Flask)**.

## Estrutura

| Caminho | Função |
|---|---|
| `app.py` | Servidor Python: página e assistente virtual (`/perguntar`) |
| `templates/index.html` | Página HTML |
| `static/style.css` | Estilos (rosa claro, com modo escuro e versão para celular) |
| `static/script.js` | Categorias, busca de tecnologias e prancha |
| `docs/index.html` | Versão estática, sem Python (para o GitHub Pages) |
| `requirements.txt` / `Procfile` | Dependências e comando de início |

## Rodar no computador

```bash
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000 no navegador.

## Publicar

**GitHub Pages (versão estática):** em *Settings → Pages*, escolha a branch `main` e a pasta `/docs`.

**PythonAnywhere (versão com Python):**
1. `git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git`
2. Aba **Web → Add a new web app → Flask**.
3. Em *Source code*, coloque `/home/SEU-USUARIO-PA/NOME-DO-REPOSITORIO`.
4. No arquivo WSGI, apague tudo e cole:

```python
import sys
caminho = "/home/SEU-USUARIO-PA/NOME-DO-REPOSITORIO"
if caminho not in sys.path:
    sys.path.insert(0, caminho)
from app import app as application
```

5. Clique em **Reload**.

## Aviso

Conteúdo educativo. A escolha de tecnologias assistivas deve ser feita com profissionais.

## Feito por

Anna Clara, Victoria Mancine, Rafaella Eduarda Santiago, Ana Luísa, Danielly Viegas, Ana Cecília, Luiza Maria, Rafaela Eduarda Silva e Luara.
