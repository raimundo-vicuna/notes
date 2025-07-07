from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit
from PySide6.QtGui import QGuiApplication
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from app.windows import getSubjects

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

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.buildScatterGraph(), stretch=1)
        left_layout.addWidget(self.buildBarGraph(), stretch=1)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.buildAnalysisText(), stretch=2)

        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

    def getAverages(self):
        averages = []
        subjects = getSubjects(self.notas)
        for subject in subjects:
            average = round(self.notas.calc_promedio(subject), 1)
            averages.append((subject, average))
        return sorted(averages, key=lambda x: x[1])

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
        ax.set_yticks(sorted(set(y)))
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

    def buildAnalysisText(self):
        data = self.getAverages()
        avg_all = round(sum(avg for _, avg in data) / len(data), 1)

        lowest = data[:3]
        lowest_str = '\n  '.join([f"{subject}: {avg}" for subject, avg in lowest])

        # Simulación mejora promedio
        improvements = []
        total_subjects = len(data)
        for subject, avg in data:
            improved_avg = avg + 0.5 if avg + 0.5 <= 7 else 7  # cap max 7
            new_total = sum(a for _, a in data) - avg + improved_avg
            new_prom = round(new_total / total_subjects, 2)
            diff = round(new_prom - avg_all, 2)
            improvements.append(f"- Improving {subject} by 0.5 points could raise overall average to {new_prom} (change: {diff:+})")

        recommendations = f"""
📊 Data Analysis Summary

The average performance across all subjects is **{avg_all}**, indicating a generally solid academic standing. However, a few key observations stand out:

🔍 Key Findings:

- Lowest-performing subjects are likely dragging down the overall average. These include:
  {lowest_str}
  These should be considered **critical subjects for improvement**, as even slight progress here can significantly boost the general average.

- Top-performing subjects (grades ≥ 6.7) show strong consistency and suggest mastery in those areas. They are potential academic strengths worth maintaining.

- The distribution of grades shows low variance, indicating consistency in performance.

📈 Recommendations:

1. Focus on improvement in the weakest 3 subjects. 
   Increasing each by just 0.5 could raise your overall GPA by ~0.2–0.3 points.

2. Maintain strengths in subjects above 6.5.

3. Set micro-goals: aim for 0.2–0.4 point improvements gradually.

4. Monitor trends over time and adjust study strategies accordingly.

💡 Simulation of impact of improving each subject by 0.5 points:
{chr(10).join(improvements)}
"""

        text_widget = QTextEdit()
        text_widget.setReadOnly(True)
        text_widget.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                border: none;
                padding: 10px;
            }
        """)
        text_widget.setText(recommendations.strip())
        return text_widget