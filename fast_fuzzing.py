import argparse
import requests
import sys
import multiprocessing
from tabulate import tabulate
import signal

def def_handler(sig, frame):
    sys.exit(0)

# CTRL_C
signal.signal(signal.SIGINT, def_handler)

# COLORS
green_colour = "\033[0;32m\033[1m"
end_colour = "\033[0m"
red_colour = "\033[0;31m\033[1m"
blue_colour = "\033[0;34m\033[1m"
yellow_colour = "\033[0;33m\033[1m"
purple_colour = "\033[0;35m\033[1m"
turquoise_colour = "\033[0;36m\033[1m"
gray_colour = "\033[0;37m\033[1m" 


print(f"""{purple_colour}
      ███████╗ █████╗ ███████╗████████╗    ███████╗██╗   ██╗███████╗███████╗██╗███╗   ██╗ ██████╗ 
      ██╔════╝██╔══██╗██╔════╝╚══██╔══╝    ██╔════╝██║   ██║╚══███╔╝╚══███╔╝██║████╗  ██║██╔════╝ 
      █████╗  ███████║███████╗   ██║       █████╗  ██║   ██║  ███╔╝   ███╔╝ ██║██╔██╗ ██║██║  ███╗
      ██╔══╝  ██╔══██║╚════██║   ██║       ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██║██║╚██╗██║██║   ██║
      ██║     ██║  ██║███████║   ██║       ██║     ╚██████╔╝███████╗███████╗██║██║ ╚████║╚██████╔╝
      ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝                                                                               
      {end_colour}""")
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True, help='URL objetivo')
parser.add_argument('-w', '--wordlist', required=True, help='Especificar ruta del diccionario')
parser.add_argument('-e', '--extensions', help='Extensiones de archivos separadas por comas: -e php, txt, py, ...')
parser.add_argument('--subdomains', action='store_true', help='Fuzzear subdominios')
parser.add_argument('-t', '--threads', type=int, help='Número de hilos a emplear')
parser.add_argument('--hc', nargs='+', type=int, help='Ocultar códigos de estado: --hc 404 301 201 ...')
args = parser.parse_args()

results = multiprocessing.Manager().list()
count = multiprocessing.Value('i', 0)

def check_url_existence(url):
    try:
        if not url.startswith('https://') and not url.startswith('http://'):
            url = 'https://' + url
        response = requests.head(url)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f'Error HTTP!')
        return False
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Error de conexión!')
        return False
    except requests.exceptions.RequestException as req_err:
        print(f'Error de solicitud!')
        return False

def fuzz_url(url, filter_codes):
    try:
        response = requests.get(url)
        if response.status_code not in filter_codes:
            results.append([url, response.status_code])
            print_table(results)
    except requests.ConnectionError as e:
        None
    except requests.Timeout as e:
        print(f'Tiempo de espera agotado: {e}')
    except requests.RequestException as e:
        print(f'Error de solicitud: {e}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

def print_table(results):
    clear_console()
    if results:
        colored_results = [[f"{yellow_colour}{url}{end_colour}", f"{blue_colour}{code}{end_colour}"] for url, code in results]
        print(tabulate(colored_results, headers=[f"{green_colour}URL{end_colour}", f"{green_colour}Código de Estado{end_colour}"], tablefmt="pretty"))
    else:
        print("No se encontraron resultados.")

    total_count = len(wordlist)
    print(f"Progreso: {count.value}/{total_count}")

def clear_console():
    print("\033[H\033[J", end="")

def main():
    global wordlist
    if not check_url_existence(args.url):
        print(f'La URL {args.url} no es válida. Por favor, verifica la URL especificada.')
        return
    try:
        with open(args.wordlist, 'r') as wordlist_file:
            wordlist = wordlist_file.read().splitlines()
    except FileNotFoundError:
        print('Archivo de lista de palabras no encontrado.')
        return

    base_url = args.url.rstrip('/')
    extensions = args.extensions.split(',') if args.extensions else ['']
    protocol = 'https://' if base_url.startswith('https') else 'http://'
    base_url = base_url.replace('https://', '').replace('http://', '')
    filter_codes = args.hc if args.hc else []
    threads_num = args.threads if args.threads else 10

    processes = []

    for word in wordlist:
        count.get_lock()
        count.value += 1
        for extension in extensions:
            if extension:
                url = f'{protocol}{base_url}/{word}.{extension}'
            else:
                url = f'{protocol}{base_url}/{word}'
            process = multiprocessing.Process(target=fuzz_url, args=(url, filter_codes))
            processes.append(process)
            process.start()

            if len(processes) >= threads_num:
                for process in processes:
                    process.join()
                processes = []

    for process in processes:
        process.join()

if __name__ == '__main__':
    try:
        main()
        print_table(results)
    except KeyboardInterrupt:
        print(f"{red_colour}\n[!] Exiting{end_colour}")
        sys.exit(0)
    except Exception as e:
        sys.exit(0)

