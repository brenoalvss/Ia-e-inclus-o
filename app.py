"""IA a Serviço da Inclusão: site em Flask (Python) com HTML, CSS e JavaScript.

O assistente virtual roda aqui em Python: o navegador envia a pergunta para
a rota /perguntar e o servidor devolve as orientações.

Para rodar:  pip install -r requirements.txt   e depois   python app.py
"""
import re
import unicodedata

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

NOTA = "Cada pessoa é única: o melhor caminho é perguntar como ela prefere ser ajudada."
SEM_RESPOSTA = (
    "Ainda não tenho uma resposta preparada para isso. Tente perguntar sobre pessoa cega, "
    "surda, cadeirante, deficiência intelectual, dificuldade de fala, palavras respeitosas "
    "ou acessibilidade em sites."
)

# w = peso do tema; k = palavras-chave (sem acento); i = orientações
BASE = [
    {
        "w": 1,
        "k": [
            "cego",
            "cega",
            "cegueira",
            "visual",
            "enxerg",
            "baixa visao"
        ],
        "i": [
            "Pergunte antes se a pessoa quer ajuda e como prefere recebê-la.",
            "Ao chegar, diga seu nome. Ao sair, avise que está saindo.",
            "Para guiar, ofereça o seu braço ou ombro, sem puxar a pessoa.",
            "Descreva o ambiente e avise sobre degraus e obstáculos.",
            "Não distraia nem faça carinho em um cão-guia em serviço.",
            "Não mude móveis de lugar sem avisar."
        ]
    },
    {
        "w": 1,
        "k": [
            "surd",
            "auditiv",
            "libras",
            "escutar",
            "ouvir"
        ],
        "i": [
            "Chame a atenção com um aceno ou um toque leve no ombro.",
            "Fique de frente, em um lugar com boa luz, sem cobrir a boca.",
            "Fale de modo natural, sem gritar e sem exagerar nos movimentos da boca.",
            "Se necessário, use escrita, o celular ou aplicativos de transcrição.",
            "Com intérprete de Libras, olhe para a pessoa e não para o intérprete.",
            "Use vídeos com legenda sempre que possível."
        ]
    },
    {
        "w": 1,
        "k": [
            "cadeir",
            "rodas",
            "fisica",
            "mobilidade",
            "andar",
            "locomo"
        ],
        "i": [
            "Pergunte antes de empurrar a cadeira. Ela faz parte do espaço pessoal da pessoa.",
            "Não se apoie na cadeira.",
            "Em conversas longas, procure ficar na altura dos olhos.",
            "Mantenha passagens livres e confira se há rampa ou elevador.",
            "Respeite as vagas e os banheiros acessíveis."
        ]
    },
    {
        "w": 1,
        "k": [
            "intelectual",
            "down",
            "aprendizagem",
            "compreender"
        ],
        "i": [
            "Use frases curtas e claras, com uma ideia de cada vez.",
            "Dê tempo para a pessoa pensar e responder.",
            "Trate a pessoa de acordo com a idade dela, sem infantilizar.",
            "Apoie a conversa com imagens, gestos ou pictogramas.",
            "Pergunte se ficou claro e explique de outro jeito, se for preciso."
        ]
    },
    {
        "w": 1,
        "k": [
            "fala",
            "comunicac",
            "gagu",
            "nao consegue falar",
            "prancha"
        ],
        "i": [
            "Tenha paciência e não complete as frases sem perguntar.",
            "Faça perguntas que possam ser respondidas com sim ou não.",
            "Ofereça uma prancha de comunicação, papel ou aplicativo, se a pessoa usar.",
            "Olhe para a pessoa enquanto ela se comunica.",
            "Se não entendeu, peça para repetir ou mostrar de outro jeito."
        ]
    },
    {
        "w": 1,
        "k": [
            "palavra",
            "termo",
            "chamar",
            "expressoes",
            "vocabulario",
            "respeitos"
        ],
        "i": [
            "Prefira “pessoa com deficiência”.",
            "Evite “portador”, “deficiente” como rótulo e “sofre de”.",
            "Fale da pessoa primeiro e da deficiência só quando for necessário.",
            "Em caso de dúvida, pergunte como ela prefere ser chamada."
        ]
    },
    {
        "w": 1,
        "k": [
            "site",
            "acessibilidade digital",
            "texto alternativo",
            "legenda",
            "contraste",
            "internet",
            "redes sociais",
            "aplicativo"
        ],
        "i": [
            "Coloque texto alternativo nas imagens para os leitores de tela.",
            "Use legendas em vídeos e, se possível, audiodescrição.",
            "Garanta bom contraste e letras legíveis.",
            "Permita navegar só com o teclado.",
            "Escreva em linguagem simples."
        ]
    },
    {
        "w": 0.3,
        "k": [
            "ajudar",
            "ajuda",
            "oferecer",
            "dicas",
            "deficiencia"
        ],
        "i": [
            "Ofereça ajuda, mas aceite a resposta se a pessoa disser que não precisa.",
            "Pergunte como ela prefere ser ajudada.",
            "Fale diretamente com a pessoa, e não com o acompanhante.",
            "Não presuma o que ela consegue ou não fazer.",
            "Para dicas mais específicas, pergunte sobre deficiência visual, auditiva, física, intelectual ou dificuldade de fala."
        ]
    },
    {
        "w": 1,
        "k": [
            " oi ",
            " ola ",
            " bom dia ",
            " boa tarde ",
            " boa noite "
        ],
        "oi": 1,
        "i": [
            "Olá! Posso dar orientações de como se comportar e ajudar de forma respeitosa. Escolha uma pergunta abaixo ou escreva a sua."
        ]
    }
]


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " " + re.sub(r"[^a-z0-9 ]", " ", texto) + " "


def escolher(pergunta):
    t = normalizar(pergunta)
    melhor, maximo = None, 0
    for tema in BASE:
        pontos = sum(1 for k in tema["k"] if k in t) * tema["w"]
        if pontos > maximo:
            melhor, maximo = tema, pontos
    return melhor


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.get_json(silent=True) or {}
    pergunta = str(dados.get("pergunta", ""))[:200]
    tema = escolher(pergunta)
    if tema is None:
        return jsonify(texto=SEM_RESPOSTA, itens=[], nota="")
    if tema.get("oi"):
        return jsonify(texto=tema["i"][0], itens=[], nota="")
    return jsonify(texto="Algumas orientações:", itens=tema["i"], nota=NOTA)


if __name__ == "__main__":
    app.run(debug=True)
