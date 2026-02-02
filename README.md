# 🕊️ Pastoral da Acolhida — Sistema de Escalas

## 📌 Sobre o projeto
Este sistema foi desenvolvido em **Flask (Python)** para apoiar a **Pastoral da Acolhida**, oferecendo uma plataforma simples e responsiva para organizar **escalas semanais de voluntários**.  
O objetivo é facilitar a comunicação, reduzir erros e dar mais autonomia tanto para os voluntários quanto para os coordenadores.

---

## ⚙️ Funcionalidades principais

### 🔑 Tela de Login
- Sistema de autenticação para coordenadores.  
- Apenas usuários autorizados podem acessar a **Área do Coordenador**.  
- Protege as funções administrativas (adição/remoção de nomes, edição de avisos extras).  
- Sessões controladas com `Flask session` e feedback via mensagens flash.

### 👥 Área do Coordenador
- Interface exclusiva para quem organiza a escala.  
- Permite: 
  - Inserir ou remover **avisos extras** por dia da semana.  
  - Gerenciar semanas futuras (até 3 semanas exibidas).  
- Feedback imediato via **mensagens flash** (que desaparecem automaticamente).

### 📅 Escala Semanal
- Adicionar e remover voluntários em horários específicos. 
- Geração automática de semanas a partir da **segunda-feira base**.  
- Exibição de dias e horários fixos (configurados em `horarios_por_dia_formatados`).  
- Caso não haja nomes, aparece a mensagem “Sem nomes” para evitar confusão.  
- Ajustes dinâmicos: exemplo, se cair em uma quarta-feira dia 28, horários extras são adicionados automaticamente.  
- Persistência da semana ativa via `localStorage` (o sistema lembra qual semana estava aberta).  
- Saudação dinâmica (“Bom dia”, “Boa tarde”, “Boa noite”, "Boa madrugada") conforme o horário.

### 📢 Avisos Extras (`extras.json`)
- Avisos permanentes vinculados a cada semana e dia.  
- Coordenador pode salvar ou remover avisos pela área administrativa.  
- Exibidos em destaque na escala.  
- Úteis para comunicar mudanças, lembretes ou observações importantes.

### ⚡ Mensagens Flash
- Usadas para feedback rápido (ex.: “Nome adicionado com sucesso”).  
- Aparecem em caixas coloridas e **somem automaticamente** após alguns segundos.  
- Mantêm a interface limpa sem sobrecarregar o usuário.

### 🎨 Responsividade
- Logo centralizado e adaptado para diferentes telas.  
- Em **desktop**: limitado a 500px de largura.  
- Em **celular**: ocupa até 90% da tela, mantendo proporção.  
- Margens ajustadas para melhor posicionamento em cada dispositivo.  
- Escala e botões adaptados para telas pequenas.

### 🗂️ Persistência dos dados
- Escalas salvas em `escala.json`.  
- Avisos extras salvos em `extras.json`.  
- Funções utilitárias para carregar e salvar JSON garantem persistência simples e legível.

---

## ♿ Acessibilidade
O sistema foi desenvolvido com atenção à acessibilidade, buscando garantir que todos os usuários possam utilizá-lo de forma confortável e inclusiva:

- **Contraste adequado**: cores escolhidas para manter boa legibilidade em diferentes dispositivos e condições de iluminação.  
- **Textos claros e hierarquia visual**: uso de títulos, listas e espaçamento para facilitar a leitura.  
- **Compatibilidade com leitores de tela**: elementos estruturados em HTML semântico (`<header>`, `<main>`, `<footer>`, `<ul>`, `<li>`) para melhor interpretação por tecnologias assistivas.  
- **Feedback visual e textual**: mensagens flash e avisos extras aparecem em destaque, garantindo que o usuário perceba as ações realizadas.  
- **Responsividade**: interface adaptada para celulares, tablets e desktops, permitindo navegação acessível em diferentes tamanhos de tela.  
- **Botões e áreas clicáveis ampliadas**: facilitando o uso por pessoas com mobilidade reduzida ou que utilizam dispositivos de toque.  

**Essas práticas tornam o sistema mais inclusivo e preparado para atender diferentes perfis de usuários, reforçando o compromisso comunitário e pastoral.**

---

## 🚀 Como executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/pastoral-acolhida.git
   
2. Instale as dependências:
   pip install flask pytz

3. Configure usuário e senha do coordenador no código:
   USUARIO_ADMIN = "USUÁRIO"
   SENHA_ADMIN = "SENHA"

4.Execute a aplicação:
  flask run

5.Acesse no navegador:
  http://localhost:5000

## 🔄 Possibilidades de adaptação
Embora tenha sido criado para a **Pastoral da Acolhida**, este sistema pode ser facilmente adaptado para outras finalidades que envolvam **organização de escalas ou equipes voluntárias**, como:

- Outras pastorais (liturgia, música, catequese).  
- Grupos comunitários (mutirões, eventos sociais).  
- Projetos escolares (plantões, monitorias).  
- Qualquer iniciativa que precise organizar pessoas em horários e dias específicos.  

---

## 🧑‍💻 Processo de desenvolvimento
Durante o desenvolvimento, utilizei bastante o **Copilot** para acelerar a escrita de código e sugerir soluções.  
No entanto, percebi que em alguns pontos havia **inconsistências ou soluções incompletas**. Para resolver isso, recorri também ao **ChatGPT**, que me ajudou a revisar, explicar linha por linha e propor ajustes mais refinados (principalmente na parte de CSS, responsividade e separação das classes).  

Essa combinação foi essencial:  
- **Copilot** → rápido para gerar código inicial.  
- **ChatGPT** → detalhado para revisar, explicar e corrigir inconsistências.  
- **Todas ferramentas gratuitas**
---

## ✨ Reflexão
Este projeto foi um aprendizado prático sobre:
- Separação de responsabilidades entre **feedback temporário** e **avisos permanentes**.  
- Uso combinado de ferramentas de IA (**Copilot + ChatGPT**) para equilibrar velocidade e consistência.  
- Importância de revisar e entender cada linha de código, especialmente em projetos que serão usados por comunidades.  
- Como pequenas melhorias visuais (**CSS, responsividade**) fazem grande diferença na experiência do usuário.  
- A relevância de pensar em **acessibilidade e inclusão** desde o início.  


