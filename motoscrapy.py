import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

class OlxCarsSelenium:
    def scrape_olx(self):
        # Configurando o Selenium
        service = Service()  # Substitua pelo caminho correto
        options = Options()

        # Desativando imagens para acelerar o carregamento da página
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", chrome_prefs)

        # Adicionando opções para lidar com SSL e GPU
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # Adicionando opção para desativar interface gráfica (headless) se necessário
        options.add_argument('--headless')

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)

        # Lista para armazenar os resultados
        results = []

        for page in range(1, 99):
            # Usando o Selenium para obter a página
            url = f'https://www.olx.com.br/autos-e-pecas/motos/estado-sp?pe=20000&ps=17100&sp=1&o={page}'
            driver.get(url)

            # Encontrando o elemento pelo ID usando XPath
            try:
                next_data_script = driver.find_element(By.XPATH, '//script[@id="__NEXT_DATA__"]')

                # Obtendo o texto do script
                html = next_data_script.get_attribute('innerHTML')

                # Imprimindo o conteúdo HTML (pode ser removido ou ajustado conforme necessário)
                print(f"HTML content for page {page}:\n{html}\n{'='*50}")

                # Convertendo HTML para JSON
                try:
                    html_json = json.loads(html)
                    cars = html_json.get('props', {}).get('pageProps', {}).get('ads', [])

                    for car in cars:
                        properties = car.get('properties', [])  # Use uma lista vazia como valor padrão se `properties` for None
                        extracted_properties = {
                            'Modelo': None,
                            'Ano': None,
                            'Quilometragem': None,
                            'Cilindrada': None,
                            'Documentação e regularização': None
                        }
                        if properties:  # Verifique se `properties` não é uma lista vazia
                            for prop in properties:
                                if prop.get('label') in extracted_properties:
                                    extracted_properties[prop['label']] = prop.get('value')
                        try:
                            price = float(car.get('price', '0').replace('R$', '').replace('.', '').replace(',', '.'))
                        except ValueError:
                            price = 0  # Se a conversão falhar, definir o preço como 0
                        if price>0 and int(extracted_properties['Quilometragem'])>500 and int(extracted_properties['Ano'])>2000:
                            results.append({
                                'title': car.get('title'),
                                'price': float(car.get('price', '0').replace('R$', '').replace('.', '').replace(',', '.')),
                                'Modelo': extracted_properties['Modelo'],
                                'Ano': extracted_properties['Ano'],
                                'Quilometragem': extracted_properties['Quilometragem'],
                                'Cilindrada': extracted_properties['Cilindrada'],
                                'Documentação e regularização': extracted_properties['Documentação e regularização']
                            })
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for page {page}: {e}")
            except Exception as e:
                print(f"Error retrieving data for page {page}: {e}")

        # Convertendo os resultados em um DataFrame do pandas
        df = pd.DataFrame(results)

        # Salvando o DataFrame em um arquivo Excel
        df.to_excel('resultados_motos4.xlsx', index=False)

        # Fechando o driver após a conclusão
        driver.quit()

# Exemplo de uso
if __name__ == "__main__":
    scraper = OlxCarsSelenium()
    scraper.scrape_olx()
