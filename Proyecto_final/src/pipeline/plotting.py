import matplotlib.pyplot as plt

def plot_linea(valores, ruta_salida):
    plt.figure()
    plt.plot(valores)
    plt.title("Gráfico de línea")
    plt.savefig(ruta_salida)
    plt.close()

def plot_histograma(valores, ruta_salida):
    plt.figure()
    plt.hist(valores)
    plt.title("Histograma")
    plt.savefig(ruta_salida)
    plt.close()
