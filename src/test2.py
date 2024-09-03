from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from numpy import arange

class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphs: Sentence Length & Word Frequencies")
        layout = QVBoxLayout(self)

        # Configuration des boutons de navigation
        button_layout = QHBoxLayout()
        self.previous_button = QPushButton("Previous Graph")
        self.previous_button.clicked.connect(self.show_previous_graph)
        self.next_button = QPushButton("Next Graph")
        self.next_button.clicked.connect(self.show_next_graph)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)

        layout.addLayout(button_layout)

        # Ajout du canvas de Matplotlib
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

        # Initialisation de l'axe pour les graphiques
        self._static_ax = self.canvas.figure.subplots()

        # Liste des noms des graphiques ajoutés
        self.graph_names = []
        self.current_graph_index = 0

    def add_graph(self, name, freq_dist1, freq_dist2, x_label, y_label, title):
        """Ajoute un graphique basé sur deux FreqDist sous la forme d'un nouvel attribut dynamique."""
        # Extraire les clés communes pour les deux FreqDist
        common_keys = list(set(freq_dist1.keys()).intersection(set(freq_dist2.keys())))
        common_keys.sort()  # Trier les clés pour un affichage cohérent

        # Extraire les fréquences correspondantes
        y_data1 = [freq_dist1[key] for key in common_keys]
        y_data2 = [freq_dist2[key] for key in common_keys]

        graph_data = (common_keys, y_data1, y_data2, x_label, y_label, title)
        setattr(self, name, graph_data)
        self.graph_names.append(name)
        self.current_graph_index = len(self.graph_names) - 1
        self.show_graph(name)

    def update_graph(self, name, freq_dist1, freq_dist2, x_label, y_label, title):
        """Met à jour un graphique existant basé sur deux FreqDist."""
        if hasattr(self, name):
            common_keys = list(set(freq_dist1.keys()).intersection(set(freq_dist2.keys())))
            common_keys.sort()

            y_data1 = [freq_dist1[key] for key in common_keys]
            y_data2 = [freq_dist2[key] for key in common_keys]

            graph_data = (common_keys, y_data1, y_data2, x_label, y_label, title)
            setattr(self, name, graph_data)
            if self.graph_names[self.current_graph_index] == name:
                self.show_graph(name)
        else:
            raise AttributeError(f"No graph named '{name}' found.")

    def show_graph(self, name):
        """Affiche un graphique basé sur le nom de l'attribut."""
        if hasattr(self, name):
            self._static_ax.clear()
            x_data, y_data1, y_data2, x_label, y_label, title = getattr(self, name)
            bar_width = 0.35
            index = arange(len(x_data))
            self._static_ax.bar(index, y_data1, bar_width, label='Text 1')
            self._static_ax.bar(index + bar_width, y_data2, bar_width, label='Text 2')

            self._static_ax.set_xlabel(x_label)
            self._static_ax.set_ylabel(y_label)
            self._static_ax.set_title(title)
            self._static_ax.set_xticks(index + bar_width / 2)
            self._static_ax.set_xticklabels(x_data, rotation=45, ha="right")
            self._static_ax.legend()
            self.canvas.draw()
        else:
            raise AttributeError(f"No graph named '{name}' found.")

    def show_previous_graph(self):
        """Affiche le graphique précédent."""
        if self.current_graph_index > 0:
            self.current_graph_index -= 1
        else:
            self.current_graph_index = len(self.graph_names) - 1
        self.show_graph(self.graph_names[self.current_graph_index])

    def show_next_graph(self):
        """Affiche le graphique suivant."""
        if self.current_graph_index < len(self.graph_names) - 1:
            self.current_graph_index += 1
        else:
            self.current_graph_index = 0
        self.show_graph(self.graph_names[self.current_graph_index])

# Exemple d'utilisation
if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    from nltk import FreqDist
    import sys

    app = QApplication(sys.argv)
    window = GraphWindow()

    # Créer deux FreqDist fictifs
    freq_dist1 = {'word1': 10, 'word2': 15, 'word3': 8, 'word4': 13, 'word5': 9}
    freq_dist2 = {'word1': 7, 'word2': 11, 'word3': 9, 'word4': 14, 'word5': 6}

    # Ajout d'un graphique de fréquence des mots
    window.add_graph("word_freq", freq_dist1, freq_dist2, "Words", "Frequency", "Word Frequency Comparison")

    window.show()
    sys.exit(app.exec_())
