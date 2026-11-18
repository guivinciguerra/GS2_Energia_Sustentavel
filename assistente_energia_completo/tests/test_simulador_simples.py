import unittest
from unittest.mock import patch
from src.calculadora import (estimar_consumo_aparelhos, calcular_economia_por_consumo,
                             obter_consumo_interativo, simular_solar_simples)


class TestSimuladorSimples(unittest.TestCase):
    def setUp(self):
        self.aparelhos = [{'nome': 'TV', 'potencia_media_w': 100, 'horas_por_dia': 4}]
        self.parametros = {'valor_evitado_por_kwh_reais': 0.85}

    def test_consumo_por_aparelhos(self):
        resultado = estimar_consumo_aparelhos([dict(self.aparelhos[0], quantidade=2)])
        self.assertAlmostEqual(resultado['consumo_kwh_mes'], 24)

    def test_conta_direta(self):
        with patch('builtins.input', side_effect=['1', '250']):
            consumo, origem = obter_consumo_interativo(self.aparelhos)
        self.assertEqual(consumo, 250)
        self.assertEqual(origem, 'informado na conta de luz')

    def test_perguntas_aparelhos(self):
        with patch('builtins.input', side_effect=['2', '2', '4']):
            consumo, origem = obter_consumo_interativo(self.aparelhos)
        self.assertEqual(consumo, 24)
        self.assertEqual(origem, 'estimado por aparelhos')

    def test_ambos_metodos_mesma_economia(self):
        r = calcular_economia_por_consumo(250, .85)
        self.assertAlmostEqual(r['economia_reais_mes'], 170)
        self.assertAlmostEqual(r['economia_reais_ano'], 2040)
        self.assertAlmostEqual(r['geracao_kwh_mes'], 200)
        with patch('builtins.input', side_effect=['1', '250', '', '']):
            interativo = simular_solar_simples(self.aparelhos, self.parametros)
        self.assertAlmostEqual(interativo['economia_reais_mes'], 170)

    def test_validacoes(self):
        with self.assertRaises(ValueError):
            estimar_consumo_aparelhos([dict(self.aparelhos[0], quantidade=1, horas_por_dia=25)])
        with self.assertRaises(ValueError):
            calcular_economia_por_consumo(-1, .85)


if __name__ == '__main__':
    unittest.main()
