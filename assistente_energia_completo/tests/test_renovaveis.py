import unittest
from pathlib import Path
from src.calculadora import calcular_solar
from src.conhecimento import carregar_conhecimento, buscar_resposta, buscar_item

RAIZ = Path(__file__).resolve().parents[1]


class TestRenovaveis(unittest.TestCase):
    def test_residencia(self):
        r = calcular_solar(3, 4.5, 30, .8, 250, .85, 14000)
        self.assertAlmostEqual(r['geracao_kwh_mes'], 324)
        self.assertAlmostEqual(r['economia_reais_mes'], 212.5)
        self.assertAlmostEqual(r['economia_reais_ano'], 2550)
        self.assertAlmostEqual(r['retorno_simples_anos'], 14000 / 2550)

    def test_centro_comunitario(self):
        r = calcular_solar(8, 4.5, 30, .8, 700, .85, 36000)
        self.assertEqual(r['geracao_kwh_mes'], 864)
        self.assertEqual(r['economia_reais_mes'], 595)
        self.assertAlmostEqual(r['retorno_simples_anos'], 36000 / 7140)

    def test_zero(self):
        r = calcular_solar(0, 4.5, 30, .8, 250, .85, 14000)
        self.assertIsNone(r['retorno_simples_anos'])

    def test_valores_invalidos(self):
        with self.assertRaises(ValueError):
            calcular_solar(3, 4.5, 30, 1.3, 250, .85, 14000)
        with self.assertRaises(ValueError):
            calcular_solar(-1, 4.5, 30, .8, 250, .85, 14000)

    def test_temas(self):
        base = carregar_conhecimento(RAIZ / 'data' / 'conhecimento_ia.json')
        for duvida in ('Como funciona energia solar?', 'E geração compartilhada?',
                       'biogas', 'aquecimento solar', 'escola', 'economia solar'):
            self.assertIsNotNone(buscar_resposta(duvida, base), duvida)
        self.assertIsNone(buscar_item('dúvida sobre basquete', base))


if __name__ == '__main__':
    unittest.main()
