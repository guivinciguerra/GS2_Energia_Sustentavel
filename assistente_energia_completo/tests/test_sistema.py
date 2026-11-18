import csv
import tempfile
import unittest
from pathlib import Path

from src.armazenamento import carregar_atendimentos, salvar_atendimentos, exportar_csv
from src.conhecimento import buscar_resposta, carregar_conhecimento, normalizar
from src.indicadores import calcular_indicadores


class TestSistema(unittest.TestCase):
    def test_normalizacao_e_busca(self):
        base = [{'palavras_chave': ['energia solar'], 'resposta': 'Resposta solar'}]
        self.assertEqual(normalizar('ElÉTrIcA'), 'eletrica')
        self.assertEqual(buscar_resposta('Como funciona ENERGIA SOLAR?', base), 'Resposta solar')
        self.assertIsNone(buscar_resposta('Pergunta desconhecida', base))

    def test_indicadores(self):
        dados = [
            {'duvida': 'a', 'encontrou': 'Sim', 'ajudou': 'Sim', 'tentativas': 1, 'tempo_segundos': 10, 'facilidade': 5},
            {'duvida': 'b', 'encontrou': 'Não', 'ajudou': 'Não', 'tentativas': 3, 'tempo_segundos': 20, 'facilidade': 3},
        ]
        ind = calcular_indicadores(dados)
        self.assertEqual(ind['respostas_encontradas_pct'], 50)
        self.assertEqual(ind['taxa_ajudou_pct'], 50)
        self.assertEqual(ind['tempo_medio_segundos'], 10)
        self.assertEqual(ind['tentativas_por_atendimento'], 2)
        self.assertEqual(ind['facilidade_media'], 4)
        self.assertEqual(ind['duvidas_sem_solucao'], ['b'])
        self.assertIsNone(calcular_indicadores([]))

    def test_json_e_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            dados = [{'data_hora': '2026-01-01 12:00:00', 'duvida': 'solar', 'encontrou': 'Sim',
                      'ajudou': 'Sim', 'tentativas': 1, 'tempo_segundos': 2.4, 'facilidade': 5}]
            salvar_atendimentos(pasta / 'data' / 'atendimentos.json', dados)
            self.assertEqual(carregar_atendimentos(pasta / 'data' / 'atendimentos.json'), dados)
            csv_path = pasta / 'data' / 'atendimentos.csv'
            exportar_csv(csv_path, dados)
            exportar_csv(csv_path, dados)  # não duplica
            with csv_path.open(encoding='utf-8-sig', newline='') as arq:
                linhas = list(csv.DictReader(arq, delimiter=';'))
            self.assertEqual(len(linhas), 1)

    def test_base_json(self):
        base = carregar_conhecimento(Path(__file__).resolve().parents[1] / 'data' / 'conhecimento_ia.json')
        self.assertGreater(len(base), 0)


if __name__ == '__main__':
    unittest.main()
