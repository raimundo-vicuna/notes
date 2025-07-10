from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QGuiApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def getSubjects(notas_obj):
    return list(notas_obj.data.keys())

class DataAnalysisWindow(QMainWindow):
    def __init__(self, notas_obj, parent=None): 
        super().__init__(parent)
        self.notas = notas_obj       
        self.setWindowTitle("Data Analysis")
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableGeometry()
        self.resize(screen_size.width() - 100, screen_size.height() - 100)
        self.build_ui()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)

        graphs_layout = QVBoxLayout()
        graphs_layout.addWidget(self.buildScatterGraph(), stretch=1)
        graphs_layout.addWidget(self.buildBarGraph(), stretch=1)
        main_layout.addLayout(graphs_layout, stretch=1)

        analysis_label = QLabel(self.getAnalysisText())
        analysis_label.setStyleSheet("color: white; font-size: 14px;")
        analysis_label.setWordWrap(True)
        main_layout.addWidget(analysis_label, stretch=2)

    def getAverages(self):
        averages = []
        subjects = getSubjects(self.notas)
        for subject in subjects:
            average = round(self.notas.calc_promedio(subject), 1)
            averages.append((subject, average))
        return sorted(averages, key=lambda x: x[1])

    def getXY(self):
        data = self.getAverages()
        x = [subject for subject, avg in data]
        y = [avg for subject, avg in data]
        return x, y

    def buildScatterGraph(self):
        data = self.getAverages()
        y = [avg for _, avg in data]
        x = list(range(1, len(y) + 1))

        fig = Figure(figsize=(3.5, 3.5), dpi=100, facecolor='#121212')
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.scatter(x, y, color='cyan', edgecolors='white', s=40)
        ax.set_facecolor('#1e1e1e')

        ax.set_xticks([])
        ax.set_yticks([round(v, 1) for v in sorted(set(y))])
        ax.tick_params(axis='y', colors='white')

        ax.set_ylim(bottom=max(min(y) - 1, 1), top=8)
        fig.tight_layout()
        return canvas

    def buildBarGraph(self):
        data = self.getAverages()
        subjects = [sub for sub, _ in data]
        values = [val for _, val in data]

        fig = Figure(figsize=(3.5, 3.5), dpi=100, facecolor='#121212')
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.bar(range(len(subjects)), values, color='cyan', edgecolor='white')
        ax.set_facecolor('#1e1e1e')

        ax.set_xticks(range(len(subjects)))
        ax.set_xticklabels(subjects, rotation=45, ha='right', color='white')

        ax.set_yticks(sorted(set(values)))
        ax.tick_params(axis='y', colors='white')
        ax.set_ylim(bottom=max(min(values) - 1, 1), top=8)

        fig.subplots_adjust(bottom=0.25)
        fig.tight_layout()
        return canvas

    def getAnalysisText(self):
        data = self.getAverages()
        subject_avgs = {subject: avg for subject, avg in data}
        lowest_subjects = sorted(subject_avgs.items(), key=lambda x: x[1])[:2]
        overall_avg = round(sum(subject_avgs.values()) / len(subject_avgs), 1)

        suggestion_lines = []
        simulated_impact = []

        for subject, current_avg in lowest_subjects:
            improved = round(current_avg + 1, 1)
            simulated_avgs = subject_avgs.copy()
            simulated_avgs[subject] = improved
            new_avg = round(sum(simulated_avgs.values()) / len(simulated_avgs), 1)
            simulated_impact.append((subject, improved, new_avg))

            suggestion_lines.append(f"<p style='margin-bottom: 10px;'>📊 <b style='color: #00ffff;'>Overall average:</b> {overall_avg}</p>")

            suggestion_lines.append("<p style='color: #00ffff;'><b>🔍 Observations:</b></p>")
            suggestion_lines.append("""
            <ul style='margin-top: 0; margin-bottom: 10px; padding-left: 20px;'>
                <li>The lowest performing subjects are likely key to improving your overall academic standing.</li>
                <li>Grades are relatively well distributed, but there's room for improvement at the lower end.</li>
            </ul>
            """)

            suggestion_lines.append("<p style='color: #00ffff;'><b>📈 Recommendations:</b></p>")
            suggestion_lines.append("<ul style='margin-top: 0; margin-bottom: 10px; padding-left: 20px;'>")
            for subject, new_grade, new_avg in simulated_impact:
                suggestion_lines.append(
                    f"<li>If you improve <b>{subject}</b> to <b>{new_grade}</b>, your general average could increase to <b>{new_avg}</b>.</li>"
                )
            suggestion_lines.append("</ul>")



        return "\n".join(suggestion_lines)
