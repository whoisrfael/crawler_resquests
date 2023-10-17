# Crawler de Links

Este é um script Python que realiza a varredura de um site a partir de uma URL raiz fornecida. O crawler irá buscar e listar todos os links encontrados, juntamente com os seus status de resposta. Além disso, ele é capaz de gerar um relatório e salvá-lo em um arquivo de texto.

## Recursos

- **Controle de Profundidade**: O crawler pode ser configurado para limitar a profundidade de varredura.
- **Limite de Requisições**: É possível definir um número máximo de requisições para evitar sobrecarregar o servidor.
- **Exclusão de Mídias**: O script ignora links que apontam para arquivos de mídia (imagens e vídeos).
- **Interface Gráfica**: A aplicação possui uma interface gráfica intuitiva para facilitar a utilização.

## Como Usar

1. Insira a URL raiz do site no campo apropriado.
2. Clique em "Iniciar Crawler" para iniciar a varredura.
3. O progresso e os resultados serão exibidos na área de relatório.
4. O relatório final pode ser salvo em um arquivo de texto.

**Observação**: Este projeto foi desenvolvido utilizando Python e as bibliotecas `requests` para fazer requisições HTTP, `BeautifulSoup` para parsing HTML e `tkinter` para a interface gráfica.
