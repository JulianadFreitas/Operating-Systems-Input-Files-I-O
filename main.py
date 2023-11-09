import time
import random

# Definição da classe Dispositivo
class Dispositivo:
    def __init__(self, nome, uso_simultaneo, tempo_operacao):
        self.nome = nome
        self.uso_simultaneo = uso_simultaneo  # Número máximo de usos simultâneos permitidos para este dispositivo
        self.tempo_operacao = tempo_operacao  # Tempo necessário para operar este dispositivo
        self.fila = []  # Fila de processos que solicitaram este dispositivo
        self.processos_bloqueados = []  # Lista de processos que estão bloqueados esperando este dispositivo

    # Método para solicitar o uso do dispositivo por um processo
    def solicitar(self, processo):
        # Se o número de processos na fila for menor que o número de usos simultâneos permitidos,
        # o processo pode usar o dispositivo imediatamente
        if len(self.fila) < self.uso_simultaneo:
            self.fila.append(processo)
            return True
        else:  # Caso contrário, o processo deve esperar
            return False

    # Método para liberar o dispositivo após o uso por um processo
    def liberar(self):
        if self.fila:
            processo = self.fila.pop(0)  # Remove o processo que terminou de usar o dispositivo da fila
            processo.ponto_bloqueio = None  # Limpa o ponto de bloqueio do processo
            self.processos_bloqueados.append(processo)  # Adiciona o processo à lista de processos bloqueados

    # Método para desbloquear processos que estavam esperando este dispositivo
    def desbloquear(self, unidade_tempo_atual):
        for processo in self.processos_bloqueados:
            # Se o processo estava bloqueado e o tempo atual é maior ou igual ao tempo em que o processo foi bloqueado mais o tempo de operação do dispositivo,
            # o processo é desbloqueado
            if processo.ponto_bloqueio is not None and unidade_tempo_atual >= processo.ponto_bloqueio + self.tempo_operacao:
                self.processos_bloqueados.remove(processo)  # Remove o processo da lista de processos bloqueados
                self.fila.append(processo)  # Adiciona o processo à fila do dispositivo
                processo.ponto_bloqueio = None  # Limpa o ponto de bloqueio do processo

class Processo:
    def __init__(self, nome, tempo_execucao, chance_requisitar_ES):
        self.nome = nome
        self.tempo_execucao = tempo_execucao  # Tempo necessário para executar este processo
        self.chance_requisitar_ES = chance_requisitar_ES  # Chance de este processo solicitar E/S
        self.ponto_bloqueio = None  # Ponto no tempo em que este processo foi bloqueado
        self.dispositivo_solicitado = None  # Dispositivo que este processo solicitou

    # Método para solicitar o uso de um dispositivo
    def solicitar_dispositivo(self, dispositivo):
        # Se o dispositivo puder ser usado imediatamente, o processo usa o dispositivo
        if dispositivo.solicitar(self):
            return True
        else:  # Caso contrário, o processo armazena o dispositivo solicitado e espera
            self.dispositivo_solicitado = dispositivo
            return False

# Função para ler o arquivo de entrada
def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas

# Função para processar as informações dos dispositivos a partir das linhas do arquivo de entrada
def processar_dispositivos(linhas):
    dispositivos_info = linhas[0].strip().split('|')
    numero_dispositivos = int(dispositivos_info[-1])
    dispositivos = []
    for i in range(1, numero_dispositivos + 1):
        dispositivo_info = linhas[i].strip().split('|')
        nome_dispositivo = dispositivo_info[0]
        uso_simultaneo = int(dispositivo_info[1])
        tempo_operacao = int(dispositivo_info[2])
        dispositivos.append(Dispositivo(nome_dispositivo, uso_simultaneo, tempo_operacao))
    return dispositivos

# Função para processar as informações do algoritmo de escalonamento a partir das linhas do arquivo de entrada
def processar_algoritmo(linhas):
    info = linhas[0].strip().split('|')
    algoritmo_escalonamento = info[0]
    fracao_CPU = int(info[1])

    return algoritmo_escalonamento, fracao_CPU

# Função para processar as informações dos processos a partir das linhas do arquivo de entrada
def processar_processos(linhas, numero_dispositivos):
    processos = []
    for linha in linhas[numero_dispositivos + 1:]:
        campos = linha.strip().split('|')
        nome_processo = campos[0]
        tempo_execucao = int(campos[2])
        chance_requisitar_ES = int(campos[-1])
        processos.append(Processo(nome_processo, tempo_execucao, chance_requisitar_ES))
    return processos

# Função para gerar informações aleatórias para simular a execução de um processo
def gerar_informacao_aleatoria(processo, dispositivos, unidade_tempo_atual, fracaoCPU):
    chance = random.randint(1, 100)
    if chance <= processo.chance_requisitar_ES:
        tempo = random.randint(1, fracaoCPU - 1)
        dispositivo = random.choice(dispositivos)
        processo.solicitar_dispositivo(dispositivo)
        processo.ponto_bloqueio = unidade_tempo_atual + tempo
        return f"Chance | {chance} | Tempo | {tempo} | Dispositivo | {dispositivo.nome}", processo.ponto_bloqueio
    else:
        return f"Chance | {chance} (Não requisitou ES)", None

# Função para executar os processos
def executar_processos(processos, dispositivos, tempo_escalonamento):
    processos_bloqueados = []
    unidade_tempo_atual = 0
    contador_global = 0
    tempo_execucao_atual = 0
    tempo_bloqueio_dispositivos = {}  # Dicionário para rastrear o tempo total de bloqueio de cada dispositivo

    for dispositivo in dispositivos:
        tempo_bloqueio_dispositivos[dispositivo.nome] = 0

    while processos:
        for dispositivo in dispositivos:
            dispositivo.desbloquear(unidade_tempo_atual)
        
        processo_em_execucao = processos.pop(0)
        informacao_aleatoria, ponto_bloqueio = gerar_informacao_aleatoria(processo_em_execucao, dispositivos, unidade_tempo_atual, tempo_escalonamento)

        if informacao_aleatoria:
            print(informacao_aleatoria)
            contador_global = 0
            tempo_execucao_atual = 0
        while processo_em_execucao.tempo_execucao > 0:
            if ponto_bloqueio is not None and unidade_tempo_atual == ponto_bloqueio:
                if processo_em_execucao.dispositivo_solicitado is not None:
                    dispositivo = processo_em_execucao.dispositivo_solicitado
                    dispositivo.liberar()
                    if processo_em_execucao.chance_requisitar_ES <= 0:
                        processos_bloqueados.append(processo_em_execucao)
                        tempo_bloqueio_dispositivos[dispositivo.nome] += dispositivo.tempo_operacao
                        print(f"{processo_em_execucao.nome} foi bloqueado no dispositivo {dispositivo.nome} por {dispositivo.tempo_operacao} unidades de tempo.")
                processo_em_execucao.dispositivo_solicitado = None
                processo_em_execucao.ponto_bloqueio = None
                break
            print(f"Tempo {unidade_tempo_atual}: {processo_em_execucao.nome} | {processo_em_execucao.tempo_execucao}")
            processo_em_execucao.tempo_execucao -= 1
            unidade_tempo_atual += 1
            contador_global += 1
            tempo_execucao_atual += 1

            if contador_global == tempo_escalonamento or tempo_execucao_atual == tempo_escalonamento:
                break
        if processo_em_execucao.tempo_execucao > 0:
            processos.append(processo_em_execucao)
        else:
            print(f"{processo_em_execucao.nome} concluído.")

    # Lidar com processos bloqueados
    for processo_bloqueado in processos_bloqueados:
        if processo_bloqueado.tempo_bloqueado > 0:
            processo_bloqueado.tempo_bloqueado -= 1
        else:
            processos.append(processo_bloqueado)

    # Exibir o tempo total que cada dispositivo ficou bloqueado
    for dispositivo, tempo_bloqueio in tempo_bloqueio_dispositivos.items():
        print(f"Tempo total de bloqueio para {dispositivo}: {tempo_bloqueio} unidades de tempo")

# Função para imprimir as informações dos dispositivos
def imprimir_informacoes_dispositivos(dispositivos):
    print("Informações dos Dispositivos:")
    for dispositivo in dispositivos:
        print("Nome do Dispositivo:", dispositivo.nome)
        print("Uso Simultâneo:", dispositivo.uso_simultaneo)
        print("Tempo de Operação:", dispositivo.tempo_operacao)
        print()

# Função principal
def main():
    nome_arquivo = 'entrada_ES.txt'
    linhas = ler_arquivo(nome_arquivo)
    dispositivos = processar_dispositivos(linhas)
    processos = processar_processos(linhas, len(dispositivos))
    algoritmo_escalonamento, fracao_cpu = processar_algoritmo(linhas)

    print(f'{algoritmo_escalonamento} | {fracao_cpu} | {len(dispositivos)}')
    executar_processos(processos, dispositivos, fracao_cpu)
    imprimir_informacoes_dispositivos(dispositivos)

# Verifica se este arquivo é o arquivo principal e, em caso afirmativo, chama a função principal
if __name__ == "__main__":
    main()