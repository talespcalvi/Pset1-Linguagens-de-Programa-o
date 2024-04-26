# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Tales Paiva Calvi   
#    Matrícula: 202305903
#    Turma: CC3M
#    Email: talespcalvi@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        """
        Função para calcular a posição dos pixels com base na coordenada (x, y), recebendo x como largura e y como altura.
        Retornará os valor de cada pixel na lista de pixels da imagem.
        """
        return self.pixels[(self.largura * y) + x]             # Foi adicionado a formula (largura * x) + y

    def set_pixel(self, x, y, c):
        """
        Função para setar o valor do pixel na imagem na coordenada (x, y), sendo x largura e y altura, e atribui a variável c para ser esse valor. 
        Esse que será setado como o valor do pixel na imagem.
        """
        self.pixels[(self.largura * y) + x] = c                # Foi adicionado a formula (largura * x) + y

    def aplicar_por_pixel(self, func):
        """
        Responsável por aplicar uma função a cada pixel da imagem e retornar uma nova imagem com os pixels atualizados de acordo com a função fornecida.
        """

        # Cria uma nova imagem que receberá o resultado das operações.
        resultado = Imagem.nova(self.largura, self.altura)     # Correção: foi alterado a posição de (self.altura, self.largura) para (self.largura, self.altura).
        
        # Loop para percorrer cada pixel da imagem.
        for x in range(self.largura):                          # Correção: Foi trocado 'resultado' por 'self'
            for y in range(self.altura):                       # Correção: Foi trocado 'resultado' por 'self'
                cor = self.get_pixel(x, y)                     # Obtém a cor do pixel na posição (x, y)
                nova_cor = func(cor)                           # Aplica a função fornecida ao pixel atual
                
                # Define a nova cor no pixel correspondente na nova imagem criada.
                resultado.set_pixel(x, y, nova_cor)            # Correção: foi alterado a posição de (y, x, nova_cor) para (x, y, nova_cor). Foi espaçado também para
                                                               # a linha ficar dentro do loop.
                
        # Retorna a nova imagem com a função já aplicada a todos pixels.
        return resultado                                       
    
    def acertar_borda(self, x, y):
         # Função para garantir que x e y estejam dentro dos limites da borda.
         x = max(0, min(x, self.largura - 1))                   # Garante que x esteja dentro do intervalo [0, largura - 1].
         y = max(0, min(y, self.altura - 1))                    # Garante que y esteja dentro do intervalo [0, altura - 1].
         return self.get_pixel(x, y)                            # Retorna a cor do pixel na posição (x, y), ajustando para os limites da imagem.
    
    def aplicar_correlacao(self, kernel):
        # Função para aplicar a correlação dos kernels nas imagens
        resultado = Imagem.nova(self.largura, self.altura)      # Cria uma nova imagem que receberá o resultado da correlação.
        tamanho_kernel = len(kernel) // 2                       # Calcula o tamanho do kernel.

        if isinstance(kernel, tuple):                           # Condicional para o uso de kernel como tupla ser funcional.
            kernel = kernel[2]

        for x in range(resultado.largura):                      # Loop para percorrer cada pixel da imagem.
            for y in range(resultado.altura):
                soma = 0.0
                for i in range(len(kernel)):                    # Loop para percorrer o kernel.
                    for j in range(len(kernel[i])):             # Calcula as coordanadas do pixel na vizinhança
                        # Calcula as coordenadas de pixels vizinhos
                        pixel_x = x - tamanho_kernel + j       
                        pixel_y = y - tamanho_kernel + i       
                         # Calcula o produto entre o valor do pixel e o valor correspondente do kernel.
                        soma += self.acertar_borda(pixel_x, pixel_y) * kernel[i][j] 
                resultado.set_pixel(x, y, soma)                 # Define o valor do pixel resultante na imagem de resultado.
        # Retorna a imagem resultante após a aplicação da correlação.
        return resultado

    def invertida(self):
        # Função para aplicar o filtro de inversão à imagem.
        return self.aplicar_por_pixel(lambda c: 255 - c)       # Correção: O valor do intervalo para um pixel é [0, 255], logo o valor 256 ultrapassa esse intervalo.

    def borrada(self, n):
        # Função para aplicar o filtro de borramento à imagem.

        # Calcula o tamanho do kernel e seus valores.
        kernel_tamanho = 1 / (n * n)                           # Ajusta o tamanho e valores do kernel
        kernel = [[kernel_tamanho for _ in range(n)] for _ in range(n)]
        resultado = self.aplicar_correlacao(kernel)            # Aplica a correlação com o kernel fornecido à imagem.

        resultado = resultado.aplicar_por_pixel(lambda c: max(min(round(c), 255), 0)) # Controla o brilho no intervalo [0, 255]
        return resultado                                       # Retorna a nova imagem com o filtro de borramento aplicado.

    def focada(self, n):
        # Função para aplicar o fitro de foco à imagem.

        # Aplica o filtro de borramento à imagem
        img_borrada = self.borrada(n)

        # Função para calcular o valor do pixel resultante
        def calcular_pixel(cor, borrada):
            # Calcula o valor do pixel resultante e controla o brilho no intervalo [0, 255]
            novo_pixel = (2 * cor - borrada)                  # Aplicação da fórmula Sx,y = round(2Ix,y - Bx,y)
            return novo_pixel

        # Aplica a função calcular_pixel a cada pixel da imagem
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):                         # Loop para percorrer cada pixel da imagem.
            for y in range(self.altura):
                # Obtém o valor do pixel na imagem original e na imagem borrada.
                cor_original = self.get_pixel(x, y)
                cor_borrada = img_borrada.get_pixel(x, y)

                # Calcula o novo valor do pixel utilizando a função calcular_pixel.
                novo_pixel = calcular_pixel(cor_original, cor_borrada)

                # Define o novo valor do pixel na imagem resultante.
                resultado.set_pixel(x, y, novo_pixel)

        resultado = resultado.aplicar_por_pixel(lambda c: max(min(round(c), 255), 0)) # Controla o brilho no intervalo [0, 255].
        # Retorna a imagem com o filtro de foco aplicado.
        return resultado

        

    def bordas(self):
        # Função para aplicar o filtro de detecção de bordas à imagem.

        # Kernel para detecção de bordas horizontais.
        kernel_kx = (3, 3,
                     [[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]])
        
        # Kernel para detecção de bordas verticais.
        kernel_ky = (3, 3,
                    [[-1, -2, -1],
                     [ 0,  0,  0],
                     [ 1,  2,  1]])
        
        # Aplica a correlação com os kernels para obter as bordas horizontais e verticais
        borda_horizontal = self.aplicar_correlacao(kernel_kx)
        borda_vertical = self.aplicar_correlacao(kernel_ky)
        resultado = Imagem.nova(self.largura, self.altura)           # Cria uma nova imagem na qual o filtro será aplicado.
        for x in range(self.largura):                                # Loop para percorrer cada pixel da imagem.
            for y in range(self.altura):
                ox = borda_horizontal.get_pixel(x, y)                # Define Ox.
                oy = borda_vertical.get_pixel(x, y)                  # Define Oy.
                oxy = math.sqrt(ox ** 2 + oy ** 2)                   # Aplica a fórmula Ox,y = round(√Ox²x,y + Oy²x,y)
                oxy = max(min(round(oxy), 255), 0)
                resultado.set_pixel(x, y, oxy)                       # Controla o brilho no intervalo [0, 255].

        # Retorna a imagem resultante com o filtro de detecção de bordas aplicado.
        return resultado
            

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.

    # i = Imagem(2, 3, [0, 50, 50, 100, 100, 255])
    # Imagem.mostrar(i)
   
    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:


    # Abaixo kernels de exemplo para testes.

    kernel_identidade = (3, 3,
                        [[0, 0, 0],
                         [0, 1, 0],
                         [0, 0, 0]])
    
    kernel_transalacao = (5, 5,
                          [[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]])
    
    kernel_media = (3, 3,
                   [[0.0, 0.2, 0.0],
                    [0.2, 0.2, 0.2],
                    [0.0, 0.2, 0.0]])

    kernel_q3 = (9, 9,
                [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    
    kernel_borrada = (3, 3,
                     [[1, 1, 1],
                      [1, 1, 1],
                      [1, 1, 1]]) 
    
    kernel_nitidez = (3, 3,
                      [[-1, -1, -1],
                       [-1, -9, -1],
                       [-1, -1, -1]])

    img = Imagem.carregar('.//test_images/construct.png')
    img_bordas = img.bordas()
    img_bordas.mostrar()
    img.mostrar()
    img_bordas.salvar('construct_BORDAS.png')

    if WINDOWS_OPENED and not sys.flags.interactive:\
        tk_root.mainloop()
